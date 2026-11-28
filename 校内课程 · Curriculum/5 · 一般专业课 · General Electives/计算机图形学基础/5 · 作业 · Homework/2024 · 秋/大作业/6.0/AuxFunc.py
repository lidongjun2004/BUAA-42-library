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
def KeyboardControl(window, eye, center, up, OriLocation, width, height):

    default_ratio=0.03 # 默认控制相机移动的比例
    ratio=default_ratio * 1280 * 828 * k / (width * height) 
    # 为了运行起来比较舒服,相机移动速率大致上和运行程序的尺寸成反比.
    # print(f"Center: {center}, Up: {up}, Eye: {eye}")
    direction = center - eye  # 视线方向
    right = np.cross(direction, up)  # 计算右方向
    right = right / np.linalg.norm(right)  # 单位化
    TranslateSpeed = ratio * np.linalg.norm(eye)  # 视野平移速度
    RotationSpeed = ratio * 10 * np.linalg.norm(eye) # 视角上下左右转动速度

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
        center = eye + (center-eye)*np.linalg.norm(direction)/np.linalg.norm(center-eye)
        up = np.cross(right, center - eye)
        up = up/np.linalg.norm(up)

    # DOWN键-低头
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        center -= RotationSpeed * up
        center = eye + (center-eye)*np.linalg.norm(direction)/np.linalg.norm(center-eye)
        up = np.cross(right, center - eye)
        up = up/np.linalg.norm(up)

    # LEFT键-左转
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        center -= RotationSpeed * right
        center = eye + (center-eye)*np.linalg.norm(direction)/np.linalg.norm(center-eye)
        right = np.cross(direction, up)
        right = right/np.linalg.norm(right)

    # RIGHT键-右转
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        center += RotationSpeed * right
        center = eye + (center-eye)*np.linalg.norm(direction)/np.linalg.norm(center-eye)
        right = np.cross(direction, up)
        right = right/np.linalg.norm(right)

    # ESC键-退出
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    # ENTER键-恢复初始视野
    if glfw.get_key(window, glfw.KEY_J) == glfw.PRESS:
        eye[:] = OriLocation[0][0]
        up[:] = OriLocation[0][1]
        center[:] = OriLocation[0][2]
        # 以上不能写 eye=OriEye因为这会让eye和OriEye指向同一片内存,使得OriEye也被修改
    
    if glfw.get_key(window, glfw.KEY_K) == glfw.PRESS:
        eye[:] = OriLocation[1][0]
        up[:] = OriLocation[1][1]
        center[:] = OriLocation[1][2]
        # 以上不能写 eye=OriEye因为这会让eye和OriEye指向同一片内存,使得OriEye也被修改

    if glfw.get_key(window, glfw.KEY_L) == glfw.PRESS:
        eye[:] = OriLocation[2][0]
        up[:] = OriLocation[2][1]
        center[:] = OriLocation[2][2]
        # 以上不能写 eye=OriEye因为这会让eye和OriEye指向同一片内存,使得OriEye也被修改
    return eye, center, up


def Terminate(): # 释放资源,终止程序
    
    # 进行解绑,并终止程序
    glUseProgram(0) # 禁用当前激活的着色器程序
    glBindTexture(GL_TEXTURE_2D, 0) # 解绑纹理
    
    glBindVertexArray(0) # 解绑VAO
    glBindBuffer(GL_ARRAY_BUFFER, 0) # 解绑VBO
    glfw.terminate()