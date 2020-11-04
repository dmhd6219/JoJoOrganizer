from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


# базовый класс для окон с крутым названием
class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.titleI = 0
        titleloop = QTimer(self)
        titleloop.timeout.connect(self.updateTitle)
        titleloop.start(50)

    # функция обновления названия окна
    def updateTitle(self):
        title = self.windowTitle()
        self.titleI = (self.titleI + 1) % len(title)
        title = "".join(
            [title[i].upper() if i == self.titleI else title[i].lower() for i in range(len(title))])
        self.setWindowTitle(title)
