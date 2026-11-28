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

def KeyboardControl(window, eye, center, up, OriEye, OriCenter, OriUp):
    ratio=0.002 # 控制视野移动的比例

    rotation_speed = ratio *np.linalg.norm(eye) # 转动速度
    vertical_speed = ratio *np.linalg.norm(eye)  # 上下移动速度
    direction = center - eye  # 视线方向
    right = np.cross(direction, up)  # 计算右方向
    right = right / np.linalg.norm(right)  # 单位化

    # WASD左右SHIFT 控制视野平移
    camera_speed = ratio * np.linalg.norm(eye)  # 调整视野平移速度

    # 按住 W 键前进
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        move = camera_speed * direction / np.linalg.norm(direction)
        eye += move
        center += move

    # 按住 S 键后退
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        move = camera_speed * direction / np.linalg.norm(direction)
        eye -= move
        center -= move

    # 按住 A 键左移
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        move = camera_speed * right
        eye -= move
        center -= move

    # 按住 D 键右移
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        move = camera_speed * right
        eye += move
        center += move

    # 按住 UP 键抬头
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        center += rotation_speed * up

    # 按住 DOWN 键低头
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        center -= rotation_speed * up

    # 左SHIFT向上移动
    if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
        move = vertical_speed * up
        eye += move
        center += move

    # 右SHIFT向下移动
    if glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS:
        move = vertical_speed * up
        eye -= move
        center -= move

    # 按住 LEFT 键左转
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        angle = np.radians(rotation_speed)
        cos_angle = np.cos(angle)
        sin_angle = np.sin(angle)
        rotation_matrix = np.array([[cos_angle, -sin_angle, 0],
                                    [sin_angle, cos_angle, 0],
                                    [0, 0, 1]])
        direction = center - eye
        new_direction = np.dot(rotation_matrix, direction)
        eye = center - new_direction

    # 按住 RIGHT 键右转
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        angle = -np.radians(rotation_speed)
        cos_angle = np.cos(angle)
        sin_angle = np.sin(angle)
        rotation_matrix = np.array([[cos_angle, -sin_angle, 0],
                                    [sin_angle, cos_angle, 0],
                                    [0, 0, 1]])
        direction = center - eye
        new_direction = np.dot(rotation_matrix, direction)
        eye = center - new_direction

    # 按下 ESC 键退出
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    # 按下 ENTER 恢复初始视野
    if glfw.get_key(window, glfw.KEY_ENTER) == glfw.PRESS:
        eye[:] = OriEye
        center[:] = OriCenter

    return eye, center


def Terminate(): # 释放资源,终止程序
    
    # 进行解绑,并终止程序
    glUseProgram(0) # 禁用当前激活的着色器程序
    glBindTexture(GL_TEXTURE_2D, 0) # 解绑纹理
    
    glBindVertexArray(0) # 解绑VAO
    glBindBuffer(GL_ARRAY_BUFFER, 0) # 解绑VBO
    glfw.terminate()