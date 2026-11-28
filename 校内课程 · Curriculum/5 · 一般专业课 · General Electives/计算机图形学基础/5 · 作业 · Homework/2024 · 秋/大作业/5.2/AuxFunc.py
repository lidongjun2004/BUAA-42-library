import numpy as np
from OpenGL.GL import *
import glfw
import math

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


k=(3-math.pow(5, 0.5))/2
def KeyboardControl(window, eye, center, up, OriEye, OriCenter, OriUp, width, height):

    default_ratio=0.003 # 默认控制相机移动的比例
    ratio=default_ratio * 1280 * 828 * k / (width * height) 
    # 为了运行起来比较舒服,相机移动速率大致上和运行程序的尺寸成反比.

    direction = center - eye  # 视线方向
    right = np.cross(direction, up)  # 计算右方向
    right = right / np.linalg.norm(right)  # 单位化
    TranslateSpeed = ratio * np.linalg.norm(eye)  # 视野平移速度
    RotationSpeed = ratio # 视角上下左右转动速度

    # I键-前进
    if glfw.get_key(window, glfw.KEY_I) == glfw.PRESS:
        move = TranslateSpeed * direction / np.linalg.norm(direction)
        eye += move
        center += move

    # O键-后退
    if glfw.get_key(window, glfw.KEY_O) == glfw.PRESS:
        move = TranslateSpeed * direction / np.linalg.norm(direction)
        eye -= move
        center -= move

    # A键-左移
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        move = TranslateSpeed * right
        eye -= move
        center -= move

    # D键-右移
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        move = TranslateSpeed * right
        eye += move
        center += move

    # W键-上移
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        move = TranslateSpeed * up
        eye += move
        center += move

    # S键-下移
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        move = TranslateSpeed * up
        eye -= move
        center -= move

    # UP键-抬头
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        center += RotationSpeed * up
        direction_new = center - eye
        direction_new = direction_new / np.linalg.norm(direction_new) * np.linalg.norm(direction)
        direction = direction_new
        center = eye + direction
        up = np.cross(right, direction)

    # DOWN键-低头
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        center -= RotationSpeed * up
        direction_new = center - eye
        direction_new = direction_new / np.linalg.norm(direction_new) * np.linalg.norm(direction)
        direction = direction_new
        center = eye + direction
        up = np.cross(right, direction)

    # LEFT键-左转
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        center -= RotationSpeed * right * 100000
        direction_new = center - eye
        direction_new = direction_new / np.linalg.norm(direction_new) * np.linalg.norm(direction)
        direction = direction_new
        center = eye + direction
        right = np.cross(direction, up)

    # RIGHT键-右转
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        center += RotationSpeed * right * 100000
        direction_new = center - eye
        direction_new = direction_new / np.linalg.norm(direction_new) * np.linalg.norm(direction)
        direction = direction_new
        center = eye + direction
        right = np.cross(direction, up)

    # ESC键-退出
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    # ENTER键-恢复初始视野
    if glfw.get_key(window, glfw.KEY_ENTER) == glfw.PRESS:
        eye[:] = OriEye
        center[:] = OriCenter
        up[:] = OriUp
        # 以上不能写 eye=OriEye因为这会让eye和OriEye指向同一片内存,使得OriEye也被修改

    return eye, center, up


def Terminate(): # 释放资源,终止程序
    
    # 进行解绑,并终止程序
    glUseProgram(0) # 禁用当前激活的着色器程序
    glBindTexture(GL_TEXTURE_2D, 0) # 解绑纹理
    
    glBindVertexArray(0) # 解绑VAO
    glBindBuffer(GL_ARRAY_BUFFER, 0) # 解绑VBO
    glfw.terminate()