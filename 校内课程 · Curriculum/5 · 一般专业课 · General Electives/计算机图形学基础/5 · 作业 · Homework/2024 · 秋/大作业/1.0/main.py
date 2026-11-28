import numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.GL import shaders


import Sphere
from AuxFunc import *
from Shader import *

# 画面长宽
width=800
height=600

# 设置帧率
TARGET_FPS = 10
frame_interval = 1.0 / TARGET_FPS


def main():
    window=CreateWindow()
    shaderProgram=CreateShader()
    
    Sun=Sphere.Planet('Sun', 1, 'Pic\Sun.jpg', shaderProgram, (0, 0, 0))
    Moon=Sphere.Planet('Moon', 1, 'Pic\Moon.jpg', shaderProgram, (2, 2, 2))
    Earth=Sphere.Planet('Earth', 1, 'Pic\Earth.jpg', shaderProgram, (-2, -2, -2))

    #设置帧率,进行渲染
    last_time=glfw.get_time()

    while not glfw.window_should_close(window):
        # 高频检查输入
        glfw.poll_events()
        check_keyboard(window)

        # 控制帧率
        current_time = glfw.get_time()
        if current_time - last_time >= frame_interval:
            last_time=glfw.get_time()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            Moon.Draw(shaderProgram)
            Sun.Draw(shaderProgram)
            Earth.Draw(shaderProgram)
            
            glfw.swap_buffers(window)
        
        # 降低CPU占用
        time.sleep(0.001)
        
    Terminate() # 无法一次删除所有VAO,VBO和Tex,只能删除目前上下文中的?待完善!
    '''
    可以通过这种方式统一管理VBO和纹理
    VBOs=[]
    VBOs.append(Moon.VBOList)
    VBOs.append(Earth.VBOList)
    '''


if __name__=='__main__':
    main()
