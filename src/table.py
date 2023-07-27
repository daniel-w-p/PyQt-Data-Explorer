import pandas as pd
from enum import Enum


class Table:
    """
    This class stores each table name and data. Creates expected data corresponding to view needs.
    """
    class DataType(Enum):
        QUANTILES = 1
        MINMAX = 2

    quantile_values = [.1, .25, .5, .75, .9]

    def __init__(self, name: str, df: pd.DataFrame):
        self.__name = name
        self.__df = df

    def __str__(self):
        return self.__name

    def get_quantiles(self, column: str):
        """
        Get percentiles of values in specified column
        :param column:
        :return: None if not numeric. If numeric data in column then return Series
        """
        if self.__df[column].dtype.kind not in 'biufc':
            unique = self.__df[column].value_counts()
            result = {"Unique values: ": len(unique)}
            for key, value in unique.items():
                result[key] = value
            return result
        else:
            return self.__df[column].quantile(self.quantile_values).to_dict()

    def get_min_mean_max(self, column: str) -> {}:
        """
        Get info about values in column as dictionary
        :param column: string name
        :return: dictionary
        """
        result = {"Rows number": self.__df[column].shape[0],
                  "NaN rows": self.__df[column].isna().sum()}
        if self.__df[column].dtype.kind in 'biufc':
            result.update({"Min value": self.__df[column].min(),
                           "Mean value": self.__df[column].mean(),
                           "Max value": self.__df[column].max()})
        return result

    def get_data(self, column: str, dt: DataType):
        """
        Get data about column by its name and type of data
        :param column: string name
        :param dt: DataType(Enum)
        :return: Data dictionary
        """
        if dt == Table.DataType.QUANTILES:
            return self.get_quantiles(column)
        elif dt == Table.DataType.MINMAX:
            return self.get_min_mean_max(column)

    def get_column_rows_as_list(self, column: str) -> []:
        return self.__df[column].to_list()

    @property
    def df(self):
        return self.__df

    @property
    def name(self) -> str:
        return self.__name

    @property
    def widget(self) -> str:
        return self.__name

    @property
    def columns_list(self) -> []:
        return self.__df.columns.to_list()

    @property
    def columns_count(self) -> int:
        return len(self.__df.columns)

    @property
    def rows_count(self) -> int:
        return len(self.__df)
