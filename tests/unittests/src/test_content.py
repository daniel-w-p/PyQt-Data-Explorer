import pandas as pd

from src import Content, Table
import pytest


class TestContent:
    @pytest.fixture
    def tables(self):
        df1 = pd.DataFrame({'col1': [1, 2, 3, 4, 5], 'col2': [0, 9, 8, 7, 6]})
        df2 = pd.DataFrame({'col3': [11, 12, 13, 14, 15], 'col4': [0, -9, -8, -7, -6]})
        table1 = Table('Tab1', df1)
        table2 = Table('Tab2', df2)
        return [table1, table2]

    def test_if_added_value_is_stored(self, tables):
        Content.set_content(tables=tables)
        assert tables == Content.get_content()
