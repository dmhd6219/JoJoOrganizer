import os, sys

from PyQt5 import QtCore
from PyQt5.Qt import QTextEdit

from windows.Window import BaseWindow
from opengl.gl import OpenGLWidget


class GLTestWindow(BaseWindow):  # тестовое окно для отладки OpenGL
    
    def __init__(self):
        super().__init__()
        width = 800
        height = 600
        self.setFixedSize(width, height)
        self.setWindowTitle("qt opengl test window")
        self.opengl = OpenGLWidget(self, width, height)
        self.show()


class PyTestWindow(BaseWindow):  # тестовое окно для общей отладки
    
    def __init__(self, parent):
        super().__init__(parent)
        width = 800
        height = 600
        self.setFixedSize(width, height)
        self.setWindowTitle("debug window")
        
        self.out = QTextEdit(self)
        self.out.move(0, 0)
        self.out.resize(width, height - 100)
        
        self.input = QTextEdit(self)
        self.input.move(0, height - 100)
        self.input.resize(width, 100)
        self.input.installEventFilter(self)
        
        self.show()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.input:
            if event.key() == QtCore.Qt.Key_Return and self.input.hasFocus():
                text = self.input.toPlainText()
                self.input.setPlainText("")
                
                res = None
                try:
                    res = eval(text)
                except BaseException as e:
                    res = e
                self.out.setPlainText(self.out.toPlainText() + "\n" + str(res))
        return super().eventFilter(obj, event)
