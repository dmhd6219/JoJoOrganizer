import sys

from PyQt5.QtWidgets import QApplication

from Windows.MainWindow import MyMainWindow

from opengl.gl import TestWindow

# основной запуск программы:)
app = QApplication(sys.argv)
ex = MyMainWindow()
ex.show()
t = TestWindow()
sys.exit(app.exec())
