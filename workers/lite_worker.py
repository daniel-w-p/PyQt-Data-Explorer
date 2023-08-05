import os
import re

import pandas as pd
import sqlite3

from src import Table


class LiteWorker:

    @staticmethod
    def export_to_sql(data_list: [Table], file_path: str):
        """
        Save all DataFrames as SQLite database
        :param data_list:  [Table]
        :param file_path: Path to save sqlite file
        """
        conn = None
        try:
            # create or/and connect to base
            conn = sqlite3.connect(file_path)

            # Save all DataFrames as tables
            for table in data_list:
                table.df.to_sql(re.sub('[ -.]', '_', table.name), conn, if_exists='replace', index=False)
        except Exception as e:
            raise e
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def import_from_sql(database) -> [Table]:
        """
        Import data from SQLite database
        :param database: string name
        :return: Dictionary {string_table_name: DataFrame_data}
        """
        data_list = []
        conn = None

        try:
            conn = sqlite3.connect(database)

            query = "SELECT name FROM sqlite_master WHERE type='table'"

            tables = pd.read_sql_query(query, conn)

            tables_names = tables['name'].to_list()

            query = "SELECT * FROM "
            # get each table as DataFrame
            for tb_name in tables_names:
                df = pd.read_sql_query(query + tb_name, conn)
                data_list.append(Table(tb_name, df))

        except Exception as e:
            raise e

        finally:
            if conn is not None:
                conn.close()

        return data_list
