import random
import time

from PyQt5.QtWidgets import QOpenGLWidget, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from OpenGL.GL import *
import glu as glutils


class TestWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 600
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("Python opengl test window")
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
        self.posX = 0
        self.posY = 0
        self.posZ = 0
        
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
    
    def wheelEvent(self, event):
        self.posZ += event.angleDelta().y() / 32
        
    def initializeGL(self):
        # lightPos = (5.0, 5.0, 10.0, 1.0)
        # glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)
        glClearColor(1, 1, 1, 1)
        glEnable(GL_DEPTH_TEST)
    
    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        glViewport((width - side) // 2, (height - side) // 2, side, side)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, +1.0, -1.0, 1.0, 5.0, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -7.0)
    
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        glRotated(self.rotationX / 16, 1.0, 0.0, 0.0)
        glRotated(self.rotationY / 16, 0.0, 1.0, 0.0)
        glRotated(self.rotationZ / 16, 0.0, 0.0, 1.0)
        glTranslated(self.posX, self.posY, self.posZ)
        self.draw()
        glPopMatrix()
    
    def onUpdate(self):
        self.update()
    
    def draw(self):        
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        
        pointData = [[0, 1, 0], [-1, -1, 0], [1, -1, 0]]
        pointColor = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        glVertexPointer(3, GL_FLOAT, 0, pointData)
        glColorPointer(3, GL_FLOAT, 0, pointColor)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        
