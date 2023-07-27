from enum import Enum

from src import Content, Table
from workers import FileWorker
from workers import LiteWorker
from workers import PostgresWorker

from PyQt6 import QtWidgets as qtw


class Engine:
    """
    This class is responsible for performing actions in the application
    """
    class DSType(Enum):
        CSV_FILE = 1
        XLSX_FILE = 2
        LITE_DB = 3
        POSTGRES_DB = 4

    def __init__(self, main_window, data_loaded_signal,
                 widget_table,
                 widget_tab_name,
                 widget_col_name,
                 widget_tables_list,
                 widget_quantiles,
                 widget_min_max,
                 widget_graph):
        self.main_window = main_window
        self.s_data_loaded = data_loaded_signal
        self.w_table = Content.WTable(widget_table)
        self.w_tab_name = Content.WLabel(widget_tab_name)
        self.w_col_name = Content.WLabel(widget_col_name)
        self.w_tables_list = Content.WList(widget_tables_list)
        self.w_quantiles = Content.WTextField(widget_quantiles, Table.DataType.QUANTILES)
        self.w_min_max = Content.WTextField(widget_min_max, Table.DataType.MINMAX)
        self.w_graph = Content.WGraph(widget_graph)

    def save_data_to_source(self, ds_type: DSType, **kwargs):
        """
        Save data to file (CSV, XLSX, SQLite) or from server (PostgreSQL)
        :param ds_type: DSType(Enum)
        :param kwargs: dictionary {path: path, filename: filename} or
        {host: host, port: port, username: user, password: pass, database: db_name}
        """
        if ds_type == self.DSType.CSV_FILE:
            result = FileWorker.save_to_csv(Content.get_table_by_name(
                self.w_tables_list.widget.currentItem().text()), kwargs['filename'])
        elif ds_type == self.DSType.XLSX_FILE:
            result = FileWorker.save_many_to_xlsx(Content.get_content(), kwargs['filename'])
        elif ds_type == self.DSType.LITE_DB:
            result = LiteWorker.export_to_sql(Content.get_content(), kwargs['filename'])
        elif ds_type == self.DSType.POSTGRES_DB:
            result = True
            # Not connect nor credentials successfully use
            if not PostgresWorker.is_ready():
                result = PostgresWorker.make_connection(host=kwargs["host"],
                                                        port=kwargs["port"],
                                                        username=kwargs["username"],
                                                        password=kwargs["password"],
                                                        database=kwargs['database'])

            if result:
                PostgresWorker.export_to_sql(Content.get_content())
            else:
                raise RuntimeWarning("Something went wrong when connecting database!")
        else:
            raise RuntimeError("Not implemented yet!")

        if result:
            qtw.QMessageBox.information(self.main_window, "Completed", "Data saved!")

    def set_content_from_source(self, ds_type: DSType, **kwargs):
        """
        Get data from file (CSV, XLSX, SQLite) or from server (PostgreSQL)
        :param ds_type: DSType(Enum)
        :param kwargs: dictionary {filename: filename} or
        {host: host, port: port, username: user, password: pass, database: db_name}
        :return:
        """
        if ds_type == self.DSType.CSV_FILE:
            data = FileWorker.read_from_csv(kwargs["filename"])
        elif ds_type == self.DSType.XLSX_FILE:
            data = FileWorker.read_from_xlsx(kwargs["filename"])
        elif ds_type == self.DSType.LITE_DB:
            data = LiteWorker.import_from_sql(kwargs["filename"])
        elif ds_type == self.DSType.POSTGRES_DB:
            result = True
            # Not connect nor credentials successfully use
            if not PostgresWorker.is_ready():
                result = PostgresWorker.make_connection(host=kwargs["host"],
                                                        port=kwargs["port"],
                                                        username=kwargs["username"],
                                                        password=kwargs["password"],
                                                        database=kwargs['database'])

            if result:
                data = PostgresWorker.import_from_sql()
            else:
                raise RuntimeWarning("Something went wrong when connecting database!")
        else:
            raise RuntimeError("Not implemented yet!")

        Content.set_content(data)
        self.s_data_loaded.emit(True)

    @staticmethod
    def are_credential_valid():
        return PostgresWorker.is_ready()

    def set_table_content(self, tab_name: str, progress_dialog: qtw.QProgressDialog):
        # This is the thread equivalent of the fill function
        self.w_table.set_table_name(tab_name)
        self.w_table.data_ready.connect(lambda val: progress_dialog.setValue(val))
        self.w_table.start()

    def set_table_name(self, tab_name: str):
        self.w_tab_name.fill(tab_name)

    def set_column_name(self, col_name: str):
        self.w_col_name.fill(col_name)

    def set_tables_list(self):
        self.w_tables_list.fill()

    def set_quantiles(self, tab_name: str, col_name: str):
        self.w_quantiles.fill(tab_name, col_name)

    def set_min_max(self, tab_name: str, col_name: str):
        self.w_min_max.fill(tab_name, col_name)

    def set_graph(self, tab_name: str, col_name: str):
        self.w_graph.fill(tab_name, col_name)

