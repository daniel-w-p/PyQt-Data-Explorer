from enum import Enum

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QDialog, QProgressDialog

from gui import Ui_DB_Dialog
from src import Engine, Content


class Slots:
    """
    This class connect Window to Engine
    """

    class FileTypes(Enum):
        CSV = 1
        XLSX = 2
        LITE = 3

    extensions = {
        FileTypes.CSV: 'CSV (*.csv)',
        FileTypes.XLSX: 'EXCEL (*.xlsx)',
        FileTypes.LITE: 'SQLite (*.db);;(*.sqlite3)'
    }

    @staticmethod
    def fill_all(engine: Engine, tab_name: str):
        """
        Fill all widgets with data from DataFrames stored as Tables in Content based on table name
        :param engine: Engine
        :param tab_name: string table name
        """
        table = Content.get_table_by_name(tab_name)
        if table is None:
            raise RuntimeWarning("Looking for Table whose name is not in the database!")

        # Loading dialog
        dialog = QProgressDialog("Loading...", None, 0, 100)
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        dialog.setWindowTitle("Please Wait")
        dialog.setAutoClose(True)
        dialog.setMinimumDuration(500)
        dialog.show()

        # Load data to widgets
        col_name = table.df.columns[0]
        engine.set_table_content(tab_name, dialog)
        engine.set_table_name(tab_name)
        Slots.fill_from_column_name(engine, tab_name, col_name)

        # dialog.close()

    @staticmethod
    def fill_from_column_name(engine: Engine, tab_name: str, col_name: str):
        """

        :param engine:
        :param tab_name:
        :param col_name:
        :return:
        """
        engine.set_column_name(col_name)
        engine.set_graph(tab_name, col_name)
        engine.set_min_max(tab_name, col_name)
        engine.set_quantiles(tab_name, col_name)

    @staticmethod
    def open_file(engine: Engine, ft: FileTypes):
        """
        Open file with data. Includes SQLite.
        :param engine: Engine
        :param ft: type of file: CSV, XLSX, LITE
        """
        file_dialog = QFileDialog.getOpenFileName(engine.main_window, 'Choose file', '', Slots.extensions[ft])
        if file_dialog[0]:
            file_path = file_dialog[0]

            if ft == Slots.FileTypes.CSV:
                engine.set_content_from_source(Engine.DSType.CSV_FILE, filename=file_path)
            elif ft == Slots.FileTypes.XLSX:
                engine.set_content_from_source(Engine.DSType.XLSX_FILE, filename=file_path)
            elif ft == Slots.FileTypes.LITE:
                engine.set_content_from_source(Engine.DSType.LITE_DB, filename=file_path)

            engine.set_tables_list()
            Slots.fill_all(engine, Content.get_first().name)

    @staticmethod
    def open_db(engine: Engine):
        """
        Open database and get data
        :param engine:
        """
        if engine.are_credential_valid():
            engine.set_content_from_source(Engine.DSType.POSTGRES_DB)

        else:
            dialog = QDialog()
            dialog_ui = Ui_DB_Dialog()
            dialog_ui.setupUi(dialog)

            if dialog.exec():
                host = dialog_ui.hostEdit.text()
                port = dialog_ui.portEdit.text()
                username = dialog_ui.userEdit.text()
                password = dialog_ui.passEdit.text()
                database = dialog_ui.baseEdit.text()

                engine.set_content_from_source(Engine.DSType.POSTGRES_DB,
                                               host=host,
                                               port=port,
                                               username=username,
                                               password=password,
                                               database=database)
                engine.set_tables_list()
                Slots.fill_all(engine, Content.get_first().name)

    @staticmethod
    def save_file(engine: Engine, ft: FileTypes):
        """
        Save file with data. Includes SQLite.
        :param engine: Engine
        :param ft: type of file: CSV, XLSX, LITE
        """
        file_dialog = QFileDialog.getSaveFileName(engine.main_window, 'Choose file', '', Slots.extensions[ft])
        if file_dialog[0]:
            file_path = file_dialog[0]

            if ft == Slots.FileTypes.CSV:
                engine.save_data_to_source(Engine.DSType.CSV_FILE, filename=file_path)
            elif ft == Slots.FileTypes.XLSX:
                engine.save_data_to_source(Engine.DSType.XLSX_FILE, filename=file_path)
            elif ft == Slots.FileTypes.LITE:
                engine.save_data_to_source(Engine.DSType.LITE_DB, filename=file_path)

    @staticmethod
    def save_db(engine: Engine):
        """
        Open database and get data
        :param engine:
        """
        if engine.are_credential_valid():
            engine.save_data_to_source(Engine.DSType.POSTGRES_DB)

        else:
            dialog = QDialog()
            dialog_ui = Ui_DB_Dialog()
            dialog_ui.setupUi(dialog)

            if dialog.exec():
                host = dialog_ui.hostEdit.text()
                port = dialog_ui.portEdit.text()
                username = dialog_ui.userEdit.text()
                password = dialog_ui.passEdit.text()
                database = dialog_ui.baseEdit.text()

                engine.save_data_to_source(Engine.DSType.POSTGRES_DB,
                                           host=host,
                                           port=port,
                                           username=username,
                                           password=password,
                                           database=database)
