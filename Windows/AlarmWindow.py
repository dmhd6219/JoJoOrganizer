from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QSound

from Windows.Window import BaseWindow
from opengl import gl
from uis import alarm
from win32api import GetSystemMetrics
import random
import time


class AlarmWindow(alarm.Ui_MainWindow, BaseWindow):
    def __init__(self, title, timess):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.name.setText(str(title))
        self.times.setText(str(timess))

        self.setWindowTitle(str(title))

        self.openGLWidget = gl.OpenGLWidget(self, 500, 500)

        music = ['ded', 'bezbab', 'problema', 'loot', 'poh', 'barbariki', 'lubimka', 'auf']

        ya = "files/" + random.choice(music) + '.wav'
        self.sound = QSound(ya)
        self.sound.play()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.sound.stop()
