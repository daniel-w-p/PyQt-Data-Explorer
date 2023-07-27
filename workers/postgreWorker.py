import re
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine, text

from src import Table
from tools.db_tools import SqlValidation as sv


class PostgresWorker:
    __host = ''
    __port = ''
    __database = ''
    __username = ''
    __password = ''
    __engine = None

    @classmethod
    def __check_credentials(cls, host: str, port: str, username: str, password: str, database='postgres') -> bool:
        """
        Check credentials and make connection
        Warning! connection remain open !!!
        :param host: string
        :param port: string
        :param username: string
        :param password: string
        :return: connection
        """
        engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(username, quote_plus(password), host, port, database))

        if engine is not None:
            cls.__host = host
            cls.__port = port
            cls.__username = username
            cls.__password = password
            cls.__engine = engine

            return True

        else:
            return False

    @classmethod
    def close_and_clear_curr_conn(cls):
        if cls.__engine is not None:
            cls.__engine = None

        cls.__host = ''
        cls.__port = ''
        cls.__username = ''
        cls.__password = ''
        cls.__database = ''

    @classmethod
    def __check_if_db_exists(cls, database: str) -> bool:
        """
        Connection remain open
        :param database: string name
        :return: True if exists False if not
        """
        if not sv.is_valid_dbname(database):
            raise 'Database name is not valid! Allowed characters are: 0-9 a-Z and _'
        if cls.__engine is not None:

            with cls.__engine.connect() as conn:
                result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = '{}'".format(database)))

                # is there any row? - True database exists
                exists = result.fetchone() is not None

            return exists
        else:
            raise RuntimeWarning('Your connection is broken. \n Please reconnect to database.')

    @classmethod
    def __create_database(cls, database: str):
        """
        Create database. Run this if sure database not exists
        :param database: string name
        """
        if not sv.is_valid_dbname(database):
            raise RuntimeWarning('Database name is not valid! Allowed characters are: 0-9 a-Z and _')
        if cls.__engine is not None:
            with cls.__engine.connect() as conn:
                conn.execution_options(isolation_level="AUTOCOMMIT")
                result = conn.execute(text("CREATE DATABASE {}".format(database)))

            return result is not None
        else:
            raise RuntimeWarning('Your connection is broken. \n Please reconnect to database.')

    @classmethod
    def __reuse_credentials(cls) -> bool:
        """
        Use credential that have successfully connected in the past to reconnect to database
        :return:
        """
        if cls.is_ready():
            try:
                return cls.__check_credentials(cls.__host, cls.__port, cls.__username, cls.__password, cls.__database)
            except Exception as e:
                raise e
        else:
            return False

    @classmethod
    def make_connection(cls, host: str, port: str, username: str, password: str, database: str) -> bool:
        """
        Make connection to database
        :param host: string
        :param port: string
        :param username: string
        :param password: string
        :param database: string
        :return: True if successfully connected, False if not
        """
        if cls.__engine is not None:
            cls.close_and_clear_curr_conn()

        try:
            is_valid_cred = cls.__check_credentials(host, port, username, password)
            if not is_valid_cred:
                return False

            is_db_exist = cls.__check_if_db_exists(database)

            if not is_db_exist:
                is_db_exist = cls.__create_database(database)

            cls.__database = database

            # Now connect to the valid database
            cls.close_and_clear_curr_conn()
            is_valid_cred = cls.__check_credentials(host, port, username, password, database)

            return is_valid_cred and is_db_exist

        except Exception as e:
            if cls.__engine is not None:
                cls.close_and_clear_curr_conn()
            raise e

    @classmethod
    def export_to_sql(cls, data_list: [Table]):
        """
        Save all DataFrames as PostgreSQL database
        :param data_list:  [Table]
        """
        if cls.__engine is None:
            if not cls.__reuse_credentials():
                raise RuntimeWarning("Can't conntect to database \n Your connection credentials are missing.")

        try:
            # Save all DataFrames as tables
            for tab in data_list:
                name = re.sub('[ -.]', '_', tab.name)
                tab.df.to_sql(name, cls.__engine, if_exists='replace', index=False)

        except Exception as e:
            raise RuntimeWarning("PostgreSQL data save failed. \n" + str(e))

        # finally:
        #     if cls.__engine is not None:
        #         cls.__engine.close()

    @classmethod
    def import_from_sql(cls) -> [Table]:
        """
        Get data from postgreSQL
        :return: dictionary with: {key: table_name, value: DataFrame}
        """
        data_list = []
        if cls.__engine is None:
            if not cls.__reuse_credentials():
                raise RuntimeWarning("Can't conntect to database \n Your connection credentials are missing.")

        try:
            query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"

            tables = pd.read_sql_query(query, cls.__engine)
            tables_names = tables['table_name'].to_list()

            # get each table as DataFrame
            for tb_name in tables_names:
                query = "SELECT * FROM \"{}\"".format(tb_name)
                df = pd.read_sql_query(query, cls.__engine)
                data_list.append(Table(tb_name, df))

        except Exception as e:
            e_text = "Can't import from database.\n Error:" + str(e)
            raise RuntimeWarning(e_text)

        # finally:
        #     if cls.__engine is not None:
        #         cls.__engine.close()

        return data_list

    @classmethod
    def is_connected(cls) -> bool:
        """
        Check if connection is established
        :return: True if already connected to database else False
        """
        return cls.__engine is not None

    @classmethod
    def is_ready(cls) -> bool:
        """
        Check if user provide valid credentials
        :return: True if credentials are set already else False
        """
        return cls.__username != '' and cls.__password != '' and cls.__database != ''
