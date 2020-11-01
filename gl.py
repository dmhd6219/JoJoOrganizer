import random
import time

from PyQt5.QtWidgets import QOpenGLWidget, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from OpenGL.GL import *


class TestWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python opengl test window")
        self.setFixedSize(800, 600)
        self.opengl = OpenGLWidget(self)
        self.show()
        
        self.titleI = 0
        titleloop = QTimer(self)
        titleloop.timeout.connect(self.updateTitle)
        titleloop.start(50)
    
     
    def updateTitle(self):
        title = self.windowTitle()
        self.titleI = (self.titleI + 1) % len(title)
        title = "".join([title[i].upper() if i == self.titleI else title[i].lower() for i in range(len(title))])
        self.setWindowTitle(title)


class OpenGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(OpenGLWidget, self).__init__(parent)
        self.resize(800, 600)
        self.move(0, 0)
        
        renderLoop = QTimer(self)
        renderLoop.timeout.connect(self.onUpdate)
        renderLoop.start(20)
    
        self.rotationX = 0
        self.rotationY = 0
        self.rotationZ = 0
    
    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        deltaX = event.x() - self.lastPos.x()
        deltaY = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.rotationX = self.rotationX + 8 * deltaY % (360 * 16)
            self.rotationY = self.rotationY + 8 * deltaX % (360 * 16)
        elif event.buttons() & Qt.RightButton:
            self.rotationX = self.rotationX + 8 * deltaY % (360 * 16)
            self.rotationZ = self.rotationZ + 8 * deltaX % (360 * 16)

        self.lastPos = event.pos()
    
    def initializeGL(self):
        # lightPos = (5.0, 5.0, 10.0, 1.0)
        # glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glClearColor(1, 1, 1, 1)
    
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        glRotated(self.rotationX / 16, 1.0, 0.0, 0.0)
        glRotated(self.rotationY / 16, 0.0, 1.0, 0.0)
        glRotated(self.rotationZ / 16, 0.0, 0.0, 1.0)
        self.draw()
        glPopMatrix()
    
    def onUpdate(self):
        self.update()
    
    def draw(self):        
        glColor3f(1, 0, 0)
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        glVertex3f(1, 0, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glVertex3f(0, 1, 1)
        glVertex3f(0, 1, 0)
        
        glEnd()
        
