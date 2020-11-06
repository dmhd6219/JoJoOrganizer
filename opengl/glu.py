from PyQt5.QtWidgets import QOpenGLWidget, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from OpenGL.GL import *

from PIL import Image
import numpy


def createShader(shaderType, source):
    shader = glCreateShader(shaderType)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader


def useShaders():
    vertex = createShader(GL_VERTEX_SHADER, """
    #version 330 core
    
    layout (location = 0) in vec3 aPos;
    layout (location = 1) in vec3 aColor;
    layout (location = 2) in vec2 aTexCoord;
    
    out vec3 ourColor;
    out vec2 TexCoord;
    
    void main() {
        gl_Position = vec4(aPos, 1.0);
        ourColor = aColor;
        TexCoord = vec2(aTexCoord.x, aTexCoord.y);
    }
    """)
    
    fragment = create_shader(GL_FRAGMENT_SHADER, """
    #version 330 core
    out vec4 FragColor;
      
    in vec3 ourColor;
    in vec2 TexCoord;
    
    uniform sampler2D ourTexture;
    
    void main() {
        FragColor = texture(ourTexture, TexCoord);
    }
    """)
    
    program = glCreateProgram()
    
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    
    glLinkProgram(program)
    glUseProgram(program)


def drawPyramid(xMin, yMin, zMin, xMax, yMax, zMax):
    glBegin(GL_TRIANGLE_FAN)
    
    glTexCoord(0.5, 0.5)
    glVertex3f(xMin + (xMax - xMin) / 2, yMin + (yMax - yMin) / 2, zMax)
    glTexCoord(0, 0)
    
    glVertex3f(xMin, yMin, zMin)
    glTexCoord(0, 1)
    glVertex3f(xMax, yMin, zMin)


    glVertex3f(xMax, yMin, zMin)
    glTexCoord(1, 1)
    glVertex3f(xMax, yMax, zMin)
    

    glVertex3f(xMax, yMax, zMin)
    glTexCoord(1, 0)
    glVertex3f(xMin, yMax, zMin)
    

    glVertex3f(xMin, yMax, zMin)
    glTexCoord(0, 0)
    glVertex3f(xMin, yMin, zMin)    
    glEnd()
    
    glBegin(GL_QUADS)
    glVertex3f(xMin, yMin, zMin)
    glVertex3f(xMin, yMax, zMin)
    glVertex3f(xMax, yMax, zMin)
    glVertex3f(xMax, yMin, zMin)
    glEnd()
    


def drawCube(xMin, yMin, zMin, xMax, yMax, zMax):
    glBegin(GL_QUADS)
    
    glTexCoord2f(0, 0)
    glVertex3f(xMin, yMax, zMax)
    glTexCoord2f(1, 0)
    glVertex3f(xMax, yMax, zMax)
    glTexCoord2f(1, 1)
    glVertex3f(xMax, yMin, zMax)
    glTexCoord2f(0, 1)
    glVertex3f(xMin, yMin, zMax)
    
    glTexCoord2f(1, 0)
    glVertex3f(xMin, yMax, zMin)
    glTexCoord2f(0, 0)
    glVertex3f(xMax, yMax, zMin)
    glTexCoord2f(0, 1)
    glVertex3f(xMax, yMin, zMin)
    glTexCoord2f(1, 1)
    glVertex3f(xMin, yMin, zMin)
    
    glTexCoord2f(0, 1)
    glVertex3f(xMin, yMax, zMax)
    glTexCoord2f(1, 1)
    glVertex3f(xMax, yMax, zMax)
    glTexCoord2f(1, 0)
    glVertex3f(xMax, yMax, yMin)
    glTexCoord2f(0, 0)
    glVertex3f(xMin, yMax, yMin)
    
    glTexCoord2f(0, 0)
    glVertex3f(xMin, yMin, zMax)
    glTexCoord2f(1, 0)
    glVertex3f(xMax, yMin, zMax)
    glTexCoord2f(1, 1)
    glVertex3f(xMax, yMin, yMin)
    glTexCoord2f(0, 1)
    glVertex3f(xMin, yMin, yMin)
    
    glTexCoord2f(1, 1)
    glVertex3f(xMax, yMin, zMax)
    glTexCoord2f(1, 0)
    glVertex3f(xMax, yMax, zMax)
    glTexCoord2f(1, 1)
    glVertex3f(xMax, yMax, zMin)
    glTexCoord2f(0, 1)
    glVertex3f(xMax, yMin, zMin)
    
    glTexCoord2f(1, 1)
    glVertex3f(xMin, yMin, zMax)
    glTexCoord2f(1, 0)
    glVertex3f(xMin, yMax, zMax)
    glTexCoord2f(1, 1)
    glVertex3f(xMin, yMax, zMin)
    glTexCoord2f(0, 1)
    glVertex3f(xMin, yMin, zMin)
    
    glEnd()
    
    
def createTexture(filename):
    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.uint8)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture
