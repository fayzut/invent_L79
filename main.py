# Главная основная форма приложения
# Выбор режима дальнейшей работы
import sqlite3
import sys
import code128
import openpyxl

from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidgetItem, QFileDialog
from openpyxl import load_workbook, Workbook
from PIL import Image

from importForm import Ui_ImportForm
# from code128 import *

DB_Name = 'inventarizaciya10.db'


# import db_view


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainWindow.ui', self)
        self.importWinBtn.clicked.connect(self.run_import_from)
        self.ViewdbBtn.clicked.connect(self.run_db_view)
        self.print_int_btn.clicked.connect(self.run_print_inv_form)

    def run_db_view(self):
        self.db_view_win = DBViewWindow()
        self.db_view_win.show()

    def run_import_from(self):
        self.importForm = ImportForm()
        self.importForm.show()

    def run_print_inv_form(self):
        self.printForm = PrintInvForm()
        self.printForm.show()


class PrintInvForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('printInvForm.ui', self)
        self.save_btn.clicked.connect(self.make_document)

    def connect_db(self):
        self.connection = sqlite3.connect(DB_Name)
        query = f"SELECT goods_name, invent_number, location_id " \
                f"FROM goods " \
            # f"WHERE {True}"
        self.res = self.connection.cursor().execute(query).fetchall()

    def make_document(self):
        self.connect_db()
        xlsx = Workbook()
        dest_filename = 'test.xlsx'
        ws1 = xlsx.active
        ws1.title = "Все позиции"

        for i, data in enumerate(self.res):
            ws1.append(data)
            # ws1.append(code128_image(data[1]))
            # ws1.append(code128.image(data[1]))

            # img = code128.image(data[1])
            # # img = Image.open('test.jpg')
            # img.anchor = 'A1'
            # ws1.add_image(img)
            # doc.add_paragraph(f"Местонахождение: {data[2]}")
            # table = doc.add_table(rows=2, cols=1)
            # table.rows[0].cells[0].text = str(data[0]).strip()
            # table.rows[0].cells[0].width = 10
            # table.rows[1].cells[0].text = str(data[1]).strip()

        # doc.add_heading(f"Инвентарные номера в {tmp_fill}")
        xlsx.save(filename=dest_filename)


class DBViewWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('db_view.ui', self)
        self.db_name = DB_Name
        # Подключение БД к таблице отображения
        # Подключение через QSqlRelationalTableModel
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.db_name)
        self.db.open()
        self.model = QSqlRelationalTableModel(self, self.db)
        self.model.setTable('goods')
        self.model.setRelation(5, QSqlRelation('statuses', 'id_status', 'status_name'))
        self.model.setRelation(6, QSqlRelation('goods_types', 'id_goods_type', 'goods_type_name'))
        self.model.setRelation(7, QSqlRelation('goods_subtypes', 'id_goods_subtype',
                                               'goods_subtype_name'))
        self.model.setRelation(8, QSqlRelation('location', 'id_location', 'location_name'))
        self.model.setRelation(9, QSqlRelation('responsibles', 'id_responsible', 'FIO'))
        self.refresh()
        self.refreshBtn.clicked.connect(self.refresh)
        self.save_all_btn.clicked.connect(self.submitall)

    # Предположительно на выходе будет закрываться БД
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def refresh(self):
        self.model.select()
        self.tableView.setModel(self.model)
        self.tableView.setItemDelegate(QSqlRelationalDelegate(self.tableView))

    def submitall(self):
        if not self.model.submitAll():
            print(self.model.lastError())
        else:
            self.refresh()


class ImportForm(QWidget, Ui_ImportForm):
    def __init__(self):
        super().__init__()
        # uic.loadUi('importForm.ui', self)
        self.setupUi(self)

        self.db_select_file_btn.clicked.connect(self.get_db_filename)
        self.source_file_btn.clicked.connect(self.get_import_filename)
        self.start_import_button.clicked.connect(self.parse_source)

    def get_db_filename(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "БД для куда импортируем")
        if file_name:
            self.db_name_edit.setText(file_name)

    def get_import_filename(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Исходные данные", "", "Excel Files (*.xlsx;*xls);;All Files (*)")
        if file_name:
            self.sheets_list_box.addItem('Loading...')
            self.source_file_edit.setText(file_name)
            self.repaint()
            # self.update()
            self.workbook = load_workbook(filename=self.source_file_edit.text())
            self.sheets_list_box.setEnabled(True)
            self.sheets_list_box.clear()
            self.sheets_list_box.addItems(self.workbook.sheetnames)
            self.sheets_list_box.setCurrentIndex(1)  # второй лист по умолчанию
            # chosen_sheet = workbook['стр.2']
            # print(chosen_sheet)
            # self.parse_source(self.sheets_list_box.currentText())

    def parse_source(self):
        the_sheet = self.workbook[self.sheets_list_box.currentText()]
        print(the_sheet['G3'].value)
        values = []
        columns = "AGH"
        row = 8
        rows_on_list = 20
        rows_between_lists = 10
        on_list = 0
        self.items_table.setColumnCount(len(columns))
        con = sqlite3.connect(self.db_name_edit.text())
        cursor = con.cursor()
        while row <= the_sheet.max_row:
            # for row in range(8, 27): #the_sheet.max_row+1):
            if on_list >= rows_on_list:
                on_list = 0
                row += rows_between_lists
            no = the_sheet[f"{columns[0]}{row}"]
            name = the_sheet[f"{columns[1]}{row}"]
            inv_num = the_sheet[f"{columns[2]}{row}"]
            if no.value and int(no.value) == len(values) + 1:
                values.append((no.value, name.value, inv_num.value))
                self.items_table.setRowCount(self.items_table.rowCount() + 1)
                for i, item in enumerate(values[-1]):
                    self.items_table.setItem(self.items_table.rowCount() - 1, i, QTableWidgetItem(
                        str(item)))
                exists_in_DB = cursor.execute(f"SELECT * FROM goods "
                                              f"WHERE invent_number='{inv_num.value}'").fetchone()
                if not exists_in_DB:
                    que = f"INSERT INTO goods(goods_name, invent_number) " \
                          f"VALUES ('{name.value}','{inv_num.value}')"
                else:
                    print(f"ВНИМАНИЕ!!! ВОЗМОЖНА Замена существующих данных!\n"
                          f"{name.value} - {inv_num.value}\n"
                          f"------------------------------")
                    que = f"UPDATE goods " \
                          f"SET goods_name = '{name.value}' " \
                          f"WHERE invent_number = '{inv_num.value}'"
                cursor.execute(que)
                con.commit()
            else:
                print(f"{no.value} != {len(values) + 1}\n"
                      f"the data is not added:\n"
                      f"{name.value},{inv_num.value}")
            row += 1
            on_list += 1
        self.items_table.repaint()
        con.close()
        # print(the_sheet['A28'].value)
        print(len(values))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
