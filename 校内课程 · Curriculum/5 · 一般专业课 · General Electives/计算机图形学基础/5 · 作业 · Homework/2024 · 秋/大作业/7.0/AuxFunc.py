# 库函数引用
import numpy as np
from OpenGL.GL import *
import glfw
import glm
import math

k=(3-math.pow(5, 0.5))/2
def KeyboardControl(window, eye, center, up, OriLocation, width, height):

    ratio=0.005 # 默认控制相机移动的速率
    TranslateSpeed = ratio * (np.linalg.norm(eye)+1000)  # 视野前后左右上下平移速度
    RotationSpeed = 2 * ratio *  (np.linalg.norm(eye)+1000) # 视角上下左右转动速度
    
    direction = center - eye  # 视线方向
    right = np.cross(direction, up)  # 计算右方向
    right = right / np.linalg.norm(right)  # 单位化
    

    # 主键盘/小键盘的加号键-前进
    if glfw.get_key(window, glfw.KEY_EQUAL) == glfw.PRESS or glfw.get_key(window, glfw.KEY_KP_ADD) == glfw.PRESS:
        move = TranslateSpeed * direction / np.linalg.norm(direction)
        eye += move
        center += move

    # 主键盘/小键盘的减号键-后退
    if glfw.get_key(window, glfw.KEY_MINUS) == glfw.PRESS or glfw.get_key(window, glfw.KEY_KP_SUBTRACT) == glfw.PRESS:
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

    # 三个设置好的初始视野,方便观察
    # X轴初始视野,按J恢复
    if glfw.get_key(window, glfw.KEY_J) == glfw.PRESS:
        eye[:] = OriLocation[0][0]
        up[:] = OriLocation[0][1]
        center[:] = OriLocation[0][2]
        # 以上不能写 eye=OriEye因为这会让eye和OriEye指向同一片内存,使得OriEye也被修改
    
    # Y轴初始视野,按K恢复
    if glfw.get_key(window, glfw.KEY_K) == glfw.PRESS:
        eye[:] = OriLocation[1][0]
        up[:] = OriLocation[1][1]
        center[:] = OriLocation[1][2]
        # 以上不能写 eye=OriEye因为这会让eye和OriEye指向同一片内存,使得OriEye也被修改

    # Z轴初始视野,按L恢复
    if glfw.get_key(window, glfw.KEY_L) == glfw.PRESS:
        eye[:] = OriLocation[2][0]
        up[:] = OriLocation[2][1]
        center[:] = OriLocation[2][2]
        # 以上不能写 eye=OriEye因为这会让eye和OriEye指向同一片内存,使得OriEye也被修改
    return eye, center, up


def FrameAdjust(fov, near, far, width, height, shaderPrograms):
    # 在窗口大小调整时，保持画面显示比例正常

    # 重新计算投影矩阵
    proj = glm.perspective(glm.radians(fov), float(width) / float(height), near, far)

    # 遍历shaderProgram并更新投影矩阵
    for shaderProgram in shaderPrograms:
        glUseProgram(shaderProgram)
        proj_loc = glGetUniformLocation(shaderProgram, "Projection")
        if proj_loc != -1:
            glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(proj))


def Terminate(): # 释放资源,终止程序
    
    glUseProgram(0) # 禁用当前激活的着色器程序
    glBindTexture(GL_TEXTURE_2D, 0) # 解绑纹理
    
    glBindVertexArray(0) # 解绑VAO
    glBindBuffer(GL_ARRAY_BUFFER, 0) # 解绑VBO
    glfw.terminate() # 终止程序