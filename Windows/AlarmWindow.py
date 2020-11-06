from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound

from Windows.Window import BaseWindow
from opengl import gl
from uis import alarm
from win32api import GetSystemMetrics
import random
import time
import wave


class AlarmWindow(alarm.Ui_MainWindow, BaseWindow):

    def __init__(self, title, timess):
        super().__init__()
        self.setupUi(self)

        self.name.setText(str(title))
        self.times.setText(str(timess))

        self.setWindowTitle(str(title))

        self.openGLWidget = gl.OpenGLWidget(self, 500, 500)

        music = ['ded', 'a4', 'barbariki', 'auf', 'lubimka', 'poh', 'wn1']

        ya = "files/" + random.choice(music) + '.wav'
        self.sound = QSound(ya)
        self.sound.play()
        
        runner = QTimer(self)
        runner.timeout.connect(self.run)
        runner.start(50)

    def run(self):
        s = QtWidgets.QApplication.instance().primaryScreen().size()
        xmax, ymax = s.width() - self.frameGeometry().width(), s.height() - self.frameGeometry().height()
        
        speed = 7
        x = self.x()
        y = self.y()
        
        deltax = random.choice([speed, -speed])
        deltay = random.choice([speed, -speed])
        
        if x + deltax < 0:
            deltax = abs(deltax)
        elif x + deltax > xmax:
            deltax = -abs(deltax)
        if y + deltay < 0:
            deltay = abs(deltay)
        elif y + deltay > ymax:
            deltay = -abs(deltay)
            
        self.move(x + deltax, y + deltay)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.sound.stop()
