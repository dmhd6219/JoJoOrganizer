from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QSurfaceFormat

from OpenGL.GL import *
<<<<<<< HEAD
from OpenGL.GLU import *
import glu as glutils
=======

from Window import BaseWindow
>>>>>>> branch 'main' of https://github.com/Chimnay/imranhello.git


class TestWindow(BaseWindow):

    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 600
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("qt opengl test window")
        self.opengl = OpenGLWidget(self)
        self.show()


class OpenGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(OpenGLWidget, self).__init__(parent)
        self.resize(800, 600)
        self.move(0, 0)
<<<<<<< HEAD
        
        format = QSurfaceFormat();  
        format.setSamples(8);
        self.setFormat(format);
        
=======

>>>>>>> branch 'main' of https://github.com/Chimnay/imranhello.git
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
            self.rotationZ = self.rotationZ + 8 * deltaX % (360 * 16)

        self.lastPos = event.pos()

    def wheelEvent(self, event):
        self.posZ += event.angleDelta().y() / 32

    def initializeGL(self):
        # lightPos = (5.0, 5.0, 10.0, 1.0)
        # glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)
        glClearColor(0.13, 0.13, 0.13, 1)
        glEnable(GL_DEPTH_TEST)
<<<<<<< HEAD
        glEnable(GL_TEXTURE_2D)
        
        self.texture = glutils.createTexture("neskvik.png")
=======
>>>>>>> branch 'main' of https://github.com/Chimnay/imranhello.git

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
<<<<<<< HEAD
        glTranslated(0.0, 0.0, -6.0)
    
=======
        glTranslated(0.0, 0.0, -7.0)

>>>>>>> branch 'main' of https://github.com/Chimnay/imranhello.git
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        glTranslated(self.posX, self.posY, self.posZ)
        glRotated(self.rotationX / 16, 1.0, 0.0, 0.0)
        glRotated(self.rotationY / 16, 0.0, 1.0, 0.0)
        glRotated(self.rotationZ / 16, 0.0, 0.0, 1.0)
        
        self.draw()
        glPopMatrix()

    def onUpdate(self):
        self.update()
<<<<<<< HEAD
    
    def draw(self):        
=======

    def draw(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        pointData = [[0, 1, 0], [-1, -1, 0], [1, -1, 0]]
        pointColor = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
>>>>>>> branch 'main' of https://github.com/Chimnay/imranhello.git

<<<<<<< HEAD
#         glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
#         glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, borderColor);  
#         glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

        glBindTexture(GL_TEXTURE_2D, self.texture)
        
        glBegin(GL_QUADS)
        glutils.drawCube(-0.5, -0.5, -0.5, 0.5, 0.5, 0.5)    
        
       
        glEnd();  

=======
        glVertexPointer(3, GL_FLOAT, 0, pointData)
        glColorPointer(3, GL_FLOAT, 0, pointColor)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
>>>>>>> branch 'main' of https://github.com/Chimnay/imranhello.git
