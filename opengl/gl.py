import random
import time

from PyQt5.QtWidgets import QOpenGLWidget, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QSurfaceFormat

from OpenGL.GL import *
from OpenGL.GLU import *
import opengl.glu as glutils


class TestWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 600
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("qt opengl test window")
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

    def __init__(self, parent=None, x=0, y=0):
        super(OpenGLWidget, self).__init__(parent)
<<<<<<< HEAD
        self.move(x, y)
        self.resize(self.window().width, self.window().height)
=======
        self.resize(500, 500)
        self.move(0, 0)
>>>>>>> branch 'main' of https://github.com/Chimnay/imranhello.git
        
        format = QSurfaceFormat();  
        format.setSamples(8);
        self.setFormat(format);
        
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
            self.rotateX(deltaY)
            self.rotateZ(deltaX)
        elif event.buttons() & Qt.RightButton:
            self.rotateY(deltaX)

        self.lastPos = event.pos()
    
    def wheelEvent(self, event):
        self.posZ += event.angleDelta().y() / 32
        
    def initializeGL(self):
        glClearColor(0.13, 0.13, 0.13, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        
<<<<<<< HEAD
        self.texture = glutils.createTexture("tex{}.png".format(random.choice([1, 2])))
        self.rotateX(-90)
=======
        self.texture = glutils.createTexture("files/neskvik.png")
>>>>>>> branch 'main' of https://github.com/Chimnay/imranhello.git

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        glViewport((width - side) // 2, (height - side) // 2, side, side)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1, +1, -1, 1, 5, 60)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslate(0, 0, -6)
    
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        glTranslated(self.posX, self.posY, self.posZ)
        glRotate(self.rotationX, 1, 0, 0)
        glRotate(self.rotationY, 0, 1, 0)
        glRotate(self.rotationZ, 0, 0, 1)
        
        self.draw()
        glPopMatrix()
    
    def onUpdate(self):
        self.update()
        self.rotateZ(8)
    
    def draw(self):        

#         glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
#         glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, borderColor);  
#         glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

        glBindTexture(GL_TEXTURE_2D, self.texture)
        glutils.drawPyramid(-0.5, -0.5, -0.5, 0.5, 0.5, 0.5)    

    def rotateX(self, deltaX):
        self.rotationX = (self.rotationX + deltaX) % 360
    
    def rotateY(self, deltaY):
        self.rotationY = (self.rotationY + deltaY) % 360
        
    def rotateZ(self, deltaZ):
        self.rotationZ = (self.rotationZ + deltaZ) % 360
    
