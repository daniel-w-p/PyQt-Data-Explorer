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

    @staticmethod
    def teardown_method():
        Content.clear()

    def test_if_added_value_is_stored(self, tables):
        Content.set(tables)
        assert tables == Content.get()

    def test_content_length(self, tables):
        assert Content.get_content_len() == 0
        Content.set(tables)
        assert Content.get_content_len() == 2

    def test_content_first_element(self, tables):
        with pytest.raises(ValueError):
            Content.get_first()
        Content.set(tables)
        assert hasattr(Content.get_first(), 'df')
        assert hasattr(Content.get_first(), 'name')

    def test_table_by_name_get_valid(self, tables):
        Content.set(tables)
        assert Content.get_table_by_name('name') is None
        assert Content.get_table_by_name('Tab1') is not None

    def test_content_tables_names_generator(self, tables):
        for idx, _ in enumerate(Content.get_names_as_generator()):
            assert False
        Content.set(tables)
        names = ['Tab1', 'Tab2']
        for idx, tab_name in enumerate(Content.get_names_as_generator()):
            assert tab_name == names[idx]

    def test_content_tables_generator(self, tables):
        for idx, _ in enumerate(Content.get_names_as_generator()):
            assert False
        Content.set(tables)
        names = ['Tab1', 'Tab2']
        for idx, tab in enumerate(Content.get_content_as_generator()):
            assert tab.name == names[idx]
