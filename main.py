import sys
from PyQt5.QtWidgets import QApplication
from windows.MainWindow import MyMainWindow


# except hook
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# основной запуск программы :)
app = QApplication(sys.argv)

mainWindow = MyMainWindow(__file__)
mainWindow.show()

sys.excepthook = except_hook

sys.exit(app.exec())
