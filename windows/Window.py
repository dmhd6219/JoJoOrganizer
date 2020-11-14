from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from utils.other import iconsdir


# базовый класс для окон с крутым названием
class BaseWindow(QMainWindow):

    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.setWindowIcon(QIcon(f'{iconsdir}/jojo.ico'))
        
        self.capsIndex = 0
        titleloop = QTimer(self)
        titleloop.timeout.connect(self.updateTitle)
        titleloop.start(50)

    # функция обновления названия окна
    def updateTitle(self):
        title = self.windowTitle()
        self.capsIndex = (self.capsIndex + 1) % len(title)
        
        newTitle = ""
        for i in range(len(title)):
            newTitle += title[i].upper() if i == self.capsIndex else title[i].lower()
        
        self.setWindowTitle(newTitle)
