import sys

from PyQt5.QtWidgets import QApplication

from MainWindow import MyMainWindow
from gl import TestWindow

app = QApplication(sys.argv)
ex = MyMainWindow()
ex.show()
gl = TestWindow()
sys.exit(app.exec())
