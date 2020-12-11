# форма для просмотра БД
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class DBViewWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('db_view.ui', self)
