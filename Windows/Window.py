from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


class BaseWindow(QMainWindow):  # базовый класс для окон с крутым названием

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('files/jojo.ico'))
        
        self.capsIndex = 0
        titleloop = QTimer(self)
        titleloop.timeout.connect(self.updateTitle)
        titleloop.start(50)

    def updateTitle(self):  # функция обновления названия окна
        title = self.windowTitle()
        self.capsIndex = (self.capsIndex + 1) % len(title)
        
        newTitle = ""
        for i in range(len(title)):
            newTitle += title[i].upper() if i == self.capsIndex else title[i].lower()
        
        self.setWindowTitle(newTitle)
