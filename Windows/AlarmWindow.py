import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QSound

from Windows.Window import BaseWindow
from opengl import gl
from uis import alarm
import random


class AlarmWindow(alarm.Ui_MainWindow, BaseWindow):
    def __init__(self, title, timess):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.name.setText(str(title))
        self.times.setText(str(timess))

        self.setWindowTitle(str(title))

        # добавление нашего обаму на опенгл виджет
        self.openGLWidget = gl.OpenGLWidget(self, 500, 500)

        # сортировка файлов с музыкой, удаление не wav
        files = list(filter(lambda x: x.endswith('.wav'), os.listdir("files/music/")))
        ya = "files/music/" + random.choice(files)
        # проигрывание музыки
        if ya:
            self.sound = QSound(ya)
            self.sound.play()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # остановка музыки при закрытии окна
        self.sound.stop()
