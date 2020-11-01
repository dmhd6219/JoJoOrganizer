from PyQt5.QtWidgets import QOpenGLWidget, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from OpenGL.GL import *


def createShader(shaderType, source):
    shader = glCreateShader(shaderType)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader


def useShaders():
    vertex = createShader(GL_VERTEX_SHADER, """
    varying vec4 vertex_color;
    
    void main(){
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        vertex_color = gl_Color;
    }
    """)
    
    fragment = create_shader(GL_FRAGMENT_SHADER, """
    varying vec4 vertex_color;
    void main() {
        gl_FragColor = vertex_color;
    }
    """)
    
    program = glCreateProgram()
    
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    
    glLinkProgram(program)
    glUseProgram(program)