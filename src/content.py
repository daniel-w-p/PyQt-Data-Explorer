import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QTextEdit, QListWidget, QLabel, QTableView, QWidget
from .table import Table


class Content:
    """
    This class is responsible for storing data and populating widgets with it.
    """
    __content: list[Table] = []

    @classmethod
    def set(cls, tables: [Table]):
        cls.__content = tables

    @classmethod
    def get(cls) -> [Table]:
        return cls.__content

    @classmethod
    def clear(cls):
        cls.__content = []

    @classmethod
    def get_content_as_generator(cls):
        return (tab for tab in cls.__content)

    @classmethod
    def get_names_as_generator(cls):
        return (tab.name for tab in cls.__content)

    @classmethod
    def get_content_len(cls) -> int:
        return len(cls.__content)

    @classmethod
    def get_first(cls) -> Table:
        if cls.get_content_len() == 0:
            raise ValueError('Content is not set!')
        return cls.__content[0]

    @classmethod
    def get_table_by_name(cls, name: str) -> Table | None:
        for tab in cls.__content:
            if tab.name == name:
                return tab
        return None

    class FromWidget:
        def __init__(self, widget: QWidget):
            self.__widget = widget

        def __str__(self):
            return self.__widget.objectName()

        @property
        def widget(self):
            return self.__widget

    class WTable(FromWidget, QThread):
        data_ready = pyqtSignal(int)

        def __init__(self, table_widget: QTableView):
            Content.FromWidget.__init__(self, table_widget)
            QThread.__init__(self)
            self.__table_obj = None
            self.__table_name = None

        def set_table_name(self, name: str):
            self.__table_name = name

        def run(self):
            self.fill(self.__table_name)

        def fill(self, name: str):
            """
            Insert data to QTableWidget
            :param name: string; name of table
            """
            if Content.get_content_len() == 0:
                raise RuntimeError("No content defined")
            self.__table_obj = Content.get_table_by_name(name)
            if self.__table_obj is None:
                return
            # Columns names
            self.widget.setUpdatesEnabled(False)

            model = QStandardItemModel()

            model.setHorizontalHeaderLabels(self.__table_obj.columns_list)

            # Add rows
            for idx, row_data in self.__table_obj.df.iterrows():
                items = [QStandardItem(str(col_data[1])) for col_data in row_data.items()]
                model.appendRow(items)
                self.data_ready.emit(int(idx / self.__table_obj.rows_count * 100))

            self.data_ready.emit(100)
            self.widget.setModel(model)
            self.widget.setUpdatesEnabled(True)

    class WTextField(FromWidget):
        def __init__(self, text_widget: QTextEdit, data_type: Table.DataType):
            super().__init__(text_widget)
            self.__data_type = data_type
            self.__data_obj = None

        def fill(self, tab_name: str, col_name: str):
            """
            Insert data from dictionary to QTextEdit
            :param tab_name: string; table name
            :param col_name: string; column name
            """
            if Content.get_content_len() == 0:
                raise RuntimeError("No content defined")
            self.widget.clear()
            self.__data_obj = Content.get_table_by_name(tab_name)
            for key, value in self.__data_obj.get_data(col_name, self.__data_type).items():
                self.widget.append("{}: \t{}\n".format(key, value))

    class WList(FromWidget):
        def __init__(self, list_widget: QListWidget):
            super().__init__(list_widget)

        def fill(self):
            """
            Insert names of available tables to QListWidget
            """
            if Content.get_content_len() == 0:
                raise RuntimeError("No content defined")
            self.widget.clear()
            for tab_name in Content.get_names_as_generator():
                self.widget.addItem(tab_name)

            self.widget.setCurrentRow(0)
            self.widget.setVisible(True)

    class WLabel(FromWidget):
        def __init__(self, label: QLabel):
            super().__init__(label)

        def fill(self, text: str):
            """
            Insert text to QLabel
            """
            self.widget.setText(text)

    class WGraph(FromWidget):
        def __init__(self, graph: pg.PlotWidget):
            super().__init__(graph)

        def __str__(self):
            return "PlotWidget"

        def fill(self, table: str, column: str):
            """
            Plot histogram based on data column if valid data types
            :param table: string; table name
            :param column: string; column name
            """
            if Content.get_content_len() == 0:
                raise RuntimeError("No content defined")

            self.widget.clear()

            data = Content.get_table_by_name(table).get_column_rows_as_list(column)

            if all(element is None or isinstance(element, (int, float, complex)) for element in data):
                counts, bins = np.histogram(data, bins=np.linspace(min(data), max(data), 50))

                width = max(data) - min(data) // 50
                bar = pg.BarGraphItem(x=bins[:-1], height=counts, width=width)
                self.widget.addItem(bar)

                self.widget.setVisible(True)
