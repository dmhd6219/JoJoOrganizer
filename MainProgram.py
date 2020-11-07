import sys
from PyQt5.QtWidgets import QApplication
from Windows.MainWindow import MyMainWindow

<<<<<<< HEAD

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
=======
# except hook
# def except_hook(cls, exception, traceback):
# sys.__excepthook__(cls, exception, traceback)
>>>>>>> branch 'main' of https://github.com/Chimnay/imranhello.git


# основной запуск программы :)
app = QApplication(sys.argv)

mainWindow = MyMainWindow()
mainWindow.show()

# sys.excepthook = except_hook

sys.exit(app.exec())
