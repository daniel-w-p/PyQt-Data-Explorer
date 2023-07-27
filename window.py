from PyQt6.QtCore import Qt

from gui import Ui_MainWindow
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
import pyqtgraph as pg

from slots import Slots
from src import Engine
from workers import PostgresWorker


class Window(qtw.QMainWindow):

    data_exists = qtc.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.graph_widget = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # create
        self.graph_widget = pg.PlotWidget(self, 'white')

        # engine
        self.engine = Engine(self, self.data_exists,
                             self.ui.tableWidget, self.ui.labelTableName, self.ui.labelColumnName,
                             self.ui.tablesList, self.ui.quantilesInfo, self.ui.valuesInfo, self.graph_widget)

        # add, setup, style, connect
        self.add_and_setup()
        self.menu_actions()
        self.other_connections()

    def add_and_setup(self):
        """
        Create and add all widgets not added in creator
        """
        # Adding graph widget
        self.graph_widget.setTitle("Data representation")
        self.ui.verticalLayout.addWidget(self.graph_widget)
        self.ui.verticalLayout.setStretch(1, 4)

        # Display those empty look more ugly than rest of widgets
        self.ui.tablesList.setVisible(False)
        self.graph_widget.setVisible(False)

        # Menu items
        self.ui.menuExportCSV.setEnabled(False)
        self.ui.menuExportExcel.setEnabled(False)

        self.ui.menuDeleteCredentials.setEnabled(False)
        self.ui.menuSaveSQLite.setEnabled(False)
        self.ui.menuSavePostgreSQL.setEnabled(False)


    # Signals emitted
    def menu_actions(self):
        """
        Make in menu signal-slot connections
        """
        self.ui.menuExit.triggered.connect(self.close)

        self.ui.menuImportCSV.triggered.connect(self.on_import_csv)
        self.ui.menuExportCSV.triggered.connect(self.on_export_csv)
        self.ui.menuImportExcel.triggered.connect(self.on_import_xlsx)
        self.ui.menuExportExcel.triggered.connect(self.on_export_xlsx)

        self.ui.menuGetSQLite.triggered.connect(self.on_sqlite_open_click)
        self.ui.menuGetPostgreSQL.triggered.connect(self.on_postgresql_open_click)

        self.ui.menuDeleteCredentials.triggered.connect(self.on_clear_cred_click)

        self.ui.menuSaveSQLite.triggered.connect(self.on_sqlite_save_click)
        self.ui.menuSavePostgreSQL.triggered.connect(self.on_postgresql_save_click)

    def other_connections(self):
        """
        Make all out of menu connections (signal-slot)
        """
        self.ui.tablesList.itemClicked.connect(self.on_list_clicked)
        self.ui.tableWidget.horizontalHeader().sectionClicked.connect(self.on_table_header_clicked)
        self.data_exists.connect(self.unlock_all_menus)

    # SLOTS
    def on_list_clicked(self, item: qtw.QListWidgetItem):
        Slots.fill_all(self.engine, item.text())

    def on_table_header_clicked(self, item_id: int):
        Slots.fill_from_column_name(self.engine, self.ui.tablesList.currentItem().text(),
                                    self.ui.tableWidget.model().headerData(item_id, Qt.Orientation.Horizontal))

    def on_import_csv(self):
        Slots.open_file(self.engine, Slots.FileTypes.CSV)

    def on_export_csv(self):
        Slots.save_file(self.engine, Slots.FileTypes.CSV)

    def on_import_xlsx(self):
        Slots.open_file(self.engine, Slots.FileTypes.XLSX)

    def on_export_xlsx(self):
        Slots.save_file(self.engine, Slots.FileTypes.XLSX)

    def on_sqlite_open_click(self):
        Slots.open_file(self.engine, Slots.FileTypes.LITE)

    def on_postgresql_open_click(self):
        Slots.open_db(self.engine)

    def on_sqlite_save_click(self):
        Slots.save_file(self.engine, Slots.FileTypes.LITE)

    def on_postgresql_save_click(self):
        Slots.save_db(self.engine)

    def unlock_all_menus(self):
        self.ui.menuExportCSV.setEnabled(True)
        self.ui.menuExportExcel.setEnabled(True)

        self.ui.menuDeleteCredentials.setEnabled(True)
        self.ui.menuSaveSQLite.setEnabled(True)
        self.ui.menuSavePostgreSQL.setEnabled(True)

    @staticmethod
    def on_clear_cred_click():
        PostgresWorker.close_and_clear_curr_conn()
