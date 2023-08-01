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

    def test_test_list_of_columns_names(self, table):
        assert table.columns_list == ['col1', 'col2']
