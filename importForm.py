# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ImportForm(object):
    def setupUi(self, ImportForm):
        ImportForm.setObjectName("ImportForm")
        ImportForm.resize(424, 509)
        self.db_name_edit = QtWidgets.QLineEdit(ImportForm)
        self.db_name_edit.setEnabled(True)
        self.db_name_edit.setGeometry(QtCore.QRect(85, 10, 290, 20))
        self.db_name_edit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.db_name_edit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.db_name_edit.setReadOnly(True)
        self.db_name_edit.setObjectName("db_name_edit")
        self.label1 = QtWidgets.QLabel(ImportForm)
        self.label1.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.label1.setObjectName("label1")
        self.db_select_file_btn = QtWidgets.QPushButton(ImportForm)
        self.db_select_file_btn.setGeometry(QtCore.QRect(380, 8, 31, 23))
        self.db_select_file_btn.setObjectName("db_select_file_btn")
        self.source_file_edit = QtWidgets.QLineEdit(ImportForm)
        self.source_file_edit.setEnabled(True)
        self.source_file_edit.setGeometry(QtCore.QRect(85, 40, 290, 20))
        self.source_file_edit.setReadOnly(True)
        self.source_file_edit.setObjectName("source_file_edit")
        self.label2 = QtWidgets.QLabel(ImportForm)
        self.label2.setGeometry(QtCore.QRect(10, 40, 91, 16))
        self.label2.setObjectName("label2")
        self.source_file_btn = QtWidgets.QPushButton(ImportForm)
        self.source_file_btn.setGeometry(QtCore.QRect(380, 38, 31, 23))
        self.source_file_btn.setObjectName("source_file_btn")
        self.sheets_list_box = QtWidgets.QComboBox(ImportForm)
        self.sheets_list_box.setGeometry(QtCore.QRect(86, 82, 231, 22))
        self.sheets_list_box.setEditable(False)
        self.sheets_list_box.setObjectName("sheets_list_box")

        self.retranslateUi(ImportForm)
        QtCore.QMetaObject.connectSlotsByName(ImportForm)

    def retranslateUi(self, ImportForm):
        _translate = QtCore.QCoreApplication.translate
        ImportForm.setWindowTitle(_translate("ImportForm", "Form"))
        self.label1.setText(_translate("ImportForm", "Файл БД"))
        self.db_select_file_btn.setText(_translate("ImportForm", "..."))
        self.label2.setText(_translate("ImportForm", "Файл откуда"))
        self.source_file_btn.setText(_translate("ImportForm", "..."))
