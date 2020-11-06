import sys

from PyQt5.QtWidgets import QApplication

from Windows.MainWindow import MyMainWindow

# except hook
# def except_hook(cls, exception, traceback):
# sys.__excepthook__(cls, exception, traceback)


# основной запуск программы:)
app = QApplication(sys.argv)
ex = MyMainWindow()
ex.show()

# sys.excepthook = except_hook

sys.exit(app.exec())
