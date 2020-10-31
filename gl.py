from PyQt5.QtWidgets import QOpenGLWidget
from OpenGL.GL import *


class OpenGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(OpenGLWidget, self).__init__(parent)
        self.resize(640, 480)
        self.move(100, 100)
        
    def initializeGL(self):
        lightPos = (5.0, 5.0, 10.0, 1.0)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        
        glEnable(GL_NORMALIZE)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        self.draw()
        glPopMatrix()
    
    def draw(self):
        glColor(1, 1, 1)
