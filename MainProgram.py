import sys

from PyQt5.QtWidgets import QApplication

from Windows.MainWindow import MyMainWindow

# основной запуск программы:)
app = QApplication(sys.argv)
ex = MyMainWindow()
ex.show()
sys.exit(app.exec())
