from window import Window
from PyQt6 import QtWidgets as qtw


def handle_exception(exc_type, exc_value, exc_traceback):
    msg_box = qtw.QMessageBox()
    msg_box.setWindowTitle('An error occurred')
    msg_box.setText(str(exc_value))
    msg_box.exec()


if __name__ == "__main__":
    import sys

    sys.excepthook = handle_exception

    app = qtw.QApplication(sys.argv)
    Form = Window()
    Form.show()
    sys.exit(app.exec())
