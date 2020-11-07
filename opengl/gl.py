import random

from OpenGL.GL import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtWidgets import QOpenGLWidget

from Windows.Window import BaseWindow
import opengl.glutils


class TestWindow(BaseWindow):  # тестовое окно для отладки OpenGL
    
    def __init__(self):
        super().__init__()
        width = 800
        height = 600
        self.setFixedSize(width, height)
        self.setWindowTitle("qt opengl test window")
        self.opengl = OpenGLWidget(self, width, height)
        self.show()


class OpenGLWidget(QOpenGLWidget):

    def __init__(self, parent=None, x=0, y=0):
        super(OpenGLWidget, self).__init__(parent)
        self.move(0, 0)
        self.resize(x, y)
        
        format = QSurfaceFormat()  # сглаживание 8x
        format.setSamples(8)
        self.setFormat(format)
        
        renderLoop = QTimer(self)  # создание цикла рендера
        renderLoop.timeout.connect(self.onUpdate)
        renderLoop.start(20)  # 0,02s (лимит 50 fps)
    
        self.rotationX = 0
        self.rotationY = 0
        self.rotationZ = 0
        self.posX = 0
        self.posY = 0
        self.posZ = 0
        
    def mousePressEvent(self, event):
        self.lastMousePos = event.pos()

    def mouseMoveEvent(self, event):
        deltaX = event.x() - self.lastMousePos.x()
        deltaY = event.y() - self.lastMousePos.y()

        if event.buttons() & Qt.LeftButton:
            self.rotateX(deltaY)
            self.rotateZ(deltaX)
        elif event.buttons() & Qt.RightButton:
            self.rotateY(deltaX)

        self.lastMousePos = event.pos()
    
    def wheelEvent(self, event):
        self.posZ += event.angleDelta().y() / 32
        
    def initializeGL(self):  # настройка openGL (выполняется однократно)
        glClearColor(0.13, 0.13, 0.13, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        
        # случайный выбор и загрузка одной из текстур
        self.texture = glutils.createTexture("files/texures/tex{}.png".format(random.choice([1, 2])))
        self.rotateX(-90)

    def resizeGL(self, width, height):  # настройка камеры (выполняется при изменении размера окна)
        if min(width, height) < 0:
            return

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1, +1, -1, 1, 5, 60)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslate(0, 0, -6)
    
    def paintGL(self):  # отрисовка кадра (выполняется циклично)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        glTranslated(self.posX, self.posY, self.posZ)
        glRotate(self.rotationX, 1, 0, 0)
        glRotate(self.rotationY, 0, 1, 0)
        glRotate(self.rotationZ, 0, 0, 1)
        
        self.draw()
        glPopMatrix()
    
    def draw(self):  # рисование объектов на каждом кадре
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glutils.drawTexturedPyramid(-0.5, -0.5, -0.5, 0.5, 0.5, 0.5)    

    def onUpdate(self):  # обновление экрана (выполняется циклично)
        self.update()
        self.rotateZ(8)

    def rotateX(self, deltaX):
        self.rotationX = (self.rotationX + deltaX) % 360
    
    def rotateY(self, deltaY):
        self.rotationY = (self.rotationY + deltaY) % 360
        
    def rotateZ(self, deltaZ):
        self.rotationZ = (self.rotationZ + deltaZ) % 360
    
