import sys

from PyQt5.QtWidgets import QApplication

from MainWindow import MyMainWindow
from gl import TestWindow


def exception_hook(exctype, value, traceback):
    sys.excepthook(exctype, value, traceback)


app = QApplication(sys.argv)
sys.excepthook = exception_hook
ex = MyMainWindow()
ex.show()
gl = TestWindow()
sys.exit(app.exec())
