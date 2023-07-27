import os
import re

import pandas as pd

from src import Table


class FileWorker:
    @staticmethod
    def read_from_csv(file_path: str) -> {Table}:
        """
        Function gets data from csv file and read it to DataFrame
        :param file_path: Path to read file
        :return: pandas.DataFrame
        """
        try:
            df = pd.read_csv(file_path)
            return [Table('default_tab', df)]
        except pd.errors.ParserError:
            raise RuntimeWarning("File parse error.")
        except Exception as e:
            raise e

    @staticmethod
    def read_from_xlsx(file_path: str) -> [Table]:
        """
        Function gets data from xlsx file and read it to DataFrame
        :param file_path: Path to read file
        :return: pandas.DataFrame
        """
        try:
            dfs = pd.read_excel(file_path, sheet_name=None)
            return [Table(name, dataframe) for name, dataframe in dfs.items()]
        except pd.errors.ParserError:
            raise RuntimeWarning("File parse error.")
        except Exception as e:
            raise e

    @staticmethod
    def save_to_csv(table: Table, file_path: str) -> bool:
        """
        Save DataFrame to *.csv file
        :param table: Table
        :param file_path: Path to save file
        """
        result = False
        try:
            table.df.to_csv(file_path, index=False)
            result = True
        except Exception as e:
            raise e
        finally:
            return result

    @staticmethod
    def save_one_to_xlsx(table: Table, file_path: str, file_name: str) -> bool:
        """
        Save one DataFrame to excel *.xlsx file
        :param table: Table
        :param file_path: Path to save file
        :param file_name: File name
        """
        result = False
        try:
            full_path = os.path.join(file_path, file_name + ".xlsx")
            table.df.to_excel(full_path, index=False)
            result = True
        except Exception as e:
            raise e
        finally:
            return result

    @staticmethod
    def save_many_to_xlsx(data_list: [Table], file_path: str):
        """
        Save DataFrame to csv file
        :param data_list: [Table]
        :param file_path: Path to save file
        """
        result = False
        try:
            writer = pd.ExcelWriter(file_path, engine='openpyxl')

            # Save each DataFrame to new sheet
            for table in data_list:
                name = re.sub('[ -.]', '_', table.name)
                table.df.to_excel(writer, sheet_name=name)  # , index=False)

            # close Excel file
            writer.close()
            result = True
        except Exception as e:
            raise e
        finally:
            return result
