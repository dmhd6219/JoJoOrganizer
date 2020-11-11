import os
import random

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtMultimedia import QSound

from windows.Window import BaseWindow
from opengl import gl
from uis import alarm
from utils import audio
from utils.other import *


class AlarmWindow(BaseWindow, alarm.Ui_MainWindow):

    def __init__(self, mainWindow, title, timess):
        super().__init__(mainWindow)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.name.setText(str(title))
        self.times.setText(str(timess))

        self.setWindowTitle(str(title))

        # добавление нашего опенгл виджета
        self.openGLWidget = gl.OpenGLWidget(self, 500, 500)

        # сортировка файлов с музыкой
        files = list(filter(lambda x: x.endswith('.wav'), os.listdir(musicdir)))
        # проигрывание музыки
        if files:
            ya = musicdir + "/" + random.choice(files)
            self.sound = QSound(ya)
            self.sound.play()
        
        # определение границ дисплея и настройка скорости тряски окна
        size = QtWidgets.QApplication.instance().primaryScreen().size()
        self.xmax = size.width() - self.frameGeometry().width()
        self.ymax = size.height() - self.frameGeometry().height()
        self.speed = 7
        
        runner = QTimer(self)
        runner.timeout.connect(self.startMoving)
        runner.start(50)  # запуск тряски каждые 0.05с

    def startMoving(self):  # движение в случайном направлении
        x = self.x()
        y = self.y()

        deltax = random.choice([self.speed, -self.speed])
        deltay = random.choice([self.speed, -self.speed])

        if x + deltax < 0:
            deltax = abs(deltax)
        elif x + deltax > self.xmax:
            deltax = -abs(deltax)
        
        if y + deltay < 0:
            deltay = abs(deltay)
        elif y + deltay > self.ymax:
            deltay = -abs(deltay)

        self.move(x + deltax, y + deltay)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.sound.stop()
