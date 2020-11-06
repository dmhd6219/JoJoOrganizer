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

        self.name.setText(str(title))
        self.times.setText(str(timess))

        self.setWindowTitle(str(title))

        self.openGLWidget = gl.OpenGLWidget(self)
