import pandas as pd

from src import Table
import pytest


class TestContent:
    @pytest.fixture
    def table(self):
        df1 = pd.DataFrame({'col1': [1, 2, 3, 4, 5], 'col2': [0, 9, 8, 7, 6]})
        return Table('Tab1', df1)

    def test_if_table_guard_name_fill(self):
        df = pd.DataFrame()
        with pytest.raises(ValueError):
            Table('', df)

    def test_list_of_columns_values(self, table):
        assert table.get_column_rows_as_list('col1') == [1, 2, 3, 4, 5]
        assert table.get_column_rows_as_list('col2') == [0, 9, 8, 7, 6]

    def test_if_data_frame_is_stored(self, table):
        assert table.df is not None

    def test_if_name_is_stored(self, table):
        assert table.name is not None and table.name is not ''

    def test_list_of_columns_names(self, table):
        assert table.columns_list == ['col1', 'col2']

    def test_number_of_columns_match(self, table):
        assert table.columns_count == 2

    def test_rows_in_dataframe_count(self, table):
        assert table.rows_count == 5

    def test_if_get_data_returns_valid_func(self, table):
        quantiles = table.get_data('col1', Table.DataType.QUANTILES)
        min_max = table.get_data('col1', Table.DataType.MINMAX)
        assert len(quantiles) == len(table.quantile_values)
        assert len(min_max) == len(table.min_max_keys)
        assert quantiles == table.get_quantiles_or_unique('col1')
        assert min_max == table.get_min_mean_max('col1')
