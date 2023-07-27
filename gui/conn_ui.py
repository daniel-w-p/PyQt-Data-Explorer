# Form implementation generated from reading ui file 'ConnDialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DB_Dialog(object):
    def setupUi(self, DB_Dialog):
        DB_Dialog.setObjectName("DB_Dialog")
        DB_Dialog.resize(360, 240)
        font = QtGui.QFont()
        font.setPointSize(10)
        DB_Dialog.setFont(font)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=DB_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(180, 190, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(parent=DB_Dialog)
        self.label.setGeometry(QtCore.QRect(50, 10, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(parent=DB_Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 40, 291, 143))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.hostEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.hostEdit.setObjectName("hostEdit")
        self.verticalLayout_2.addWidget(self.hostEdit)
        self.portEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.portEdit.setObjectName("portEdit")
        self.verticalLayout_2.addWidget(self.portEdit)
        self.baseEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.baseEdit.setObjectName("baseEdit")
        self.verticalLayout_2.addWidget(self.baseEdit)
        self.userEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.userEdit.setObjectName("userEdit")
        self.verticalLayout_2.addWidget(self.userEdit)
        self.passEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.passEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.passEdit.setObjectName("passEdit")
        self.verticalLayout_2.addWidget(self.passEdit)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(DB_Dialog)
        self.buttonBox.accepted.connect(DB_Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(DB_Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DB_Dialog)

    def retranslateUi(self, DB_Dialog):
        _translate = QtCore.QCoreApplication.translate
        DB_Dialog.setWindowTitle(_translate("DB_Dialog", "Database connection"))
        self.label.setText(_translate("DB_Dialog", "Enter data"))
        self.label_2.setText(_translate("DB_Dialog", "Host"))
        self.label_3.setText(_translate("DB_Dialog", "Port"))
        self.label_4.setText(_translate("DB_Dialog", "Database"))
        self.label_5.setText(_translate("DB_Dialog", "Username"))
        self.label_6.setText(_translate("DB_Dialog", "Password"))