import sqlite3
import sys
import csv

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from untitled import Ui_MainWindow
import gl

class DBSample(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.newEvent.clicked.connect(self.add_event)
        self.deleteEvent.clicked.connect(self.delete_event)
        opengl = gl.OpenGLWidget(self)

    def add_event(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem('event1'))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem('66:66'))

    def delete_event(self):
        print(self.tableWidget.cursor())
        


def exception_hook(exctype, value, traceback):
    sys.excepthook(exctype, value, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = exception_hook
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())
