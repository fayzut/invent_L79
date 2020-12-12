# Главная основная форма приложения
# Выбор режима дальнейшей работы
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidgetItem, QFileDialog
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

DB_Name = 'inventarizaciya10.db'


# import db_view


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainWindow.ui', self)
        self.importWinBtn.clicked.connect(self.run_import_from)
        self.ViewdbBtn.clicked.connect(self.run_db_view)

    def run_db_view(self):
        self.db_view_win = DBViewWindow()
        self.db_view_win.show()

    def run_import_from(self):
        self.importForm = ImportForm()
        self.importForm.show()


class DBViewWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('db_view.ui', self)
        self.db_name = DB_Name
        self.refresh()
        self.refreshBtn.clicked.connect(self.refresh)

    def refresh(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM goods""").fetchall()
        cur.close()
        con.close()
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


class ImportForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('importForm.ui', self)
        self.db_select_file_btn.clicked.connect(self.get_db_filename)
        self.source_file_btn.clicked.connect(self.get_import_filename)

    def get_db_filename(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "БД для куда импортируем")
        if file_name:
            self.db_name_edit.setText(file_name)

    def get_import_filename(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Исходные данные", "", "Excel Files (*.xlsx;*xls);;All Files (*)")
        if file_name:
            self.source_file_edit.setText(file_name)
            self.parse_source()

    def parse_source(self):
        workbook = load_workbook(filename=self.source_file_edit.text())
        sheet_ranges = workbook['стр.2']
        print(sheet_ranges['G3'].value)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
