import sqlite3
import sys
import csv
import random

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from design import Ui_MainWindow
import gl

class DBSample(Ui_mainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.addEvent.clicked.connect(self.add_event)
        self.deleteEvent.clicked.connect(self.delete_event)
        opengl = gl.OpenGLWidget(self)

    def add_event(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0,
                                 QTableWidgetItem(f'event1{random.randint(0, 666)}'))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(f'66:66'))

    def delete_event(self):
        if self.tableWidget.selectedItems():
            while self.tableWidget.selectedItems():
                self.tableWidget.removeRow(self.tableWidget.selectedItems()[0].row())


def exception_hook(exctype, value, traceback):
    sys.excepthook(exctype, value, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = exception_hook
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())
