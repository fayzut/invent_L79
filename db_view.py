# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'db_view.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DB_View_Form(object):
    def setupUi(self, DB_View_Form):
        DB_View_Form.setObjectName("DB_View_Form")
        DB_View_Form.resize(755, 672)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(DB_View_Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.refreshBtn = QtWidgets.QPushButton(DB_View_Form)
        self.refreshBtn.setObjectName("refreshBtn")
        self.horizontalLayout.addWidget(self.refreshBtn)
        self.save_all_btn = QtWidgets.QPushButton(DB_View_Form)
        self.save_all_btn.setObjectName("save_all_btn")
        self.horizontalLayout.addWidget(self.save_all_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(DB_View_Form)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(DB_View_Form)
        QtCore.QMetaObject.connectSlotsByName(DB_View_Form)

    def retranslateUi(self, DB_View_Form):
        _translate = QtCore.QCoreApplication.translate
        DB_View_Form.setWindowTitle(_translate("DB_View_Form", "Просморт БД"))
        self.refreshBtn.setText(_translate("DB_View_Form", "Обновить"))
        self.save_all_btn.setText(_translate("DB_View_Form", "Сохранить"))
