import numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.GL import shaders
import glfw
import glm 
import time

def check_gl_error():
    err = glGetError()
    if err != GL_NO_ERROR:
        print(f"OpenGL Error: {err}")

def check_keyboard(window):
    # 按下ESC键则终止程序
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def framebuffer_size_callback(window, width:int, height:int):
    # 调整窗口大小
    glViewport(0, 0, width, height)


def Terminate(): # 释放资源,终止程序
    
    # 进行解绑,并终止程序
    glUseProgram(0) # 禁用当前激活的着色器程序
    glBindTexture(GL_TEXTURE_2D, 0) # 解绑纹理
    
    glBindVertexArray(0) # 解绑VAO
    glBindBuffer(GL_ARRAY_BUFFER, 0) # 解绑VBO
    glfw.terminate()