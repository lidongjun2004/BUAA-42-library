from OpenGL.GL import *
import os # 调整纹理文件路径分隔符,Win/Mac都可以使用

import Sphere
from AuxFunc import *
from Shader import *

# 画面长宽
width=800
height=600

# 设置帧率
TARGET_FPS = 10
frame_interval = 1.0 / TARGET_FPS

# 相机参数
eye=np.array([20, 0, 0], np.float32)
up=np.array([0, 0, 1], np.float32)
center=np.array([0, 0, 0], np.float32)

# 光线参数
LightPos = np.array([0.0, 0.0, 0.0], np.float32)      #设置光源位置
LightColor = np.array([1.0, 1.0, 1.0], np.float32) #设置光源亮度

Planet_data = {'Mercury':[2.440,5.7910000,87.9693],
               'Venus':[6.073,10.8208930,224.70],
               'Earth':[6378,14.9600000,365],
               'Mars':[6794,22.7940000,686.98],
               'Jupiter':[142984,77.8330000,4332.589],
               'Saturn':[119300,142.7000000,10759.5],
               'Uranus':[51800,286.9000000,84.32*365],
               'Neptune':[49532,450.0000000,164.8*365],
               }

def main():
    window=CreateWindow(width, height)
    Planet_shaderProgram=CreateShader(eye, center, up, LightPos, LightColor)
    SunShaderProgram=CreateSunShader()
    Sun = Sphere.Planet('Sun', 3, os.path.join('Pic', 'Sun.jpg'), SunShaderProgram, (0, 0, 0))

    Mercury = Sphere.Planet('Mercury', Planet_data['Mercury'][0], os.path.join('Pic', 'Mercury.jpg'), Planet_shaderProgram, (0, Planet_data['Mercury'][1], 0))
    Venus = Sphere.Planet('Venus', Planet_data['Venus'][0], os.path.join('Pic', 'Venus.jpg'), Planet_shaderProgram, (0, Planet_data['Venus'][1], 0))
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
            
            Sun.Draw(width, height, SunShaderProgram, eye, up, center)
            Mercury.Draw(width, height, Planet_shaderProgram, eye, up, center)
            Venus.Draw(width, height, Planet_shaderProgram, eye, up, center)
            # Neptune.Draw(shaderProgram, eye, up, center)
            
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
