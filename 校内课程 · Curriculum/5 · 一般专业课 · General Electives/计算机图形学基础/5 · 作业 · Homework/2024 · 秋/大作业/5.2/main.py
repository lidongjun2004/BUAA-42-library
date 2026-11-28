from OpenGL.GL import *
import os # 调整纹理文件路径分隔符,Win/Mac都可以使用

import Sphere
from AuxFunc import *
from Shader import *
import time

# 相关参数设置
# 设置帧率
TARGET_FPS = 20
frame_interval = 1.0 / TARGET_FPS

# 当前相机参数
# eye=np.array([0, 0, 50000], np.float32)
# up=np.array([1, 0, 0], np.float32)
# center=np.array([0, 0, 0], np.float32)

eye=np.array([50000, 0, 0], np.float32)
up=np.array([0, 0, 1], np.float32)
center=np.array([0, 0, 0], np.float32)

# 初始相机参数
OriEye=np.array([50000, 0, 0], np.float32)
OriUp=np.array([0, 0, 1], np.float32)
OriCenter=np.array([0, 0, 0], np.float32)

# 光线参数
LightPos = np.array([0.0, 0.0, 0.0], np.float32)      #设置光源位置
LightColor = np.array([1.0, 1.0, 1.0], np.float32) #设置光源亮度

Planet_data = {'Mercury':[2440, 57910000, 87.9693*24, 58.65*24],
               'Venus':[6073, 108208930, 224.70*24, -243*24],
               'Earth':[6378, 149600000, 365*24,24],
               'Mars':[6794, 227940000, 686.98*24, 24.5],
               'Jupiter':[142984, 778330000, 4332.589*24, 10],
               'Saturn':[119300, 1427000000, 10759.5*24, 10.6],
               'Uranus':[51800, 2869000000, 84.32*365*24, 17.25],
               'Neptune':[49532, 4500000000, 164.8*365*24, 16.1],
               }

#----------------------------------------------------------
# 初始化窗口和着色器程序
window, width, height=CreateWindow() #运行窗口大小正比于屏幕高(height)宽(width)比
PlanetShaderProgram=CreateShader(eye, center, up, LightPos, LightColor) # 行星着色器
StarShaderProgram=CreateStarShader() # 恒星着色器

#----------------------------------------------------------
# 初始化行星对象
Sun = Sphere.Planet('Sun', 695700, os.path.join('Pic', 'Sun.jpg'), StarShaderProgram, (0, 0, 0), 0, 0)
planets = []
k, c= 10, 1e7 # 调整轨道比例的参数
for name, data in Planet_data.items():
    planets.append(Sphere.Planet(name, data[0], os.path.join('Pic', f"{name}.jpg"), PlanetShaderProgram, (0, (data[1]) ** 0.48, 0), data[2], data[3]))

#----------------------------------------------------------
#设置帧率,进行渲染
last_time=glfw.get_time()

while not glfw.window_should_close(window):
    # 高频检查键盘输入
    glfw.poll_events()
    
    eye, center, up = KeyboardControl(window, eye, center, up, OriEye, OriCenter, OriUp, width, height) # 更新此时的视角

    # 控制帧率,渲染
    current_time = glfw.get_time()
    if current_time - last_time >= frame_interval:
        last_time=glfw.get_time()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        Sun.Draw(width, height, eye, up, center)
        for planet in planets:
            planet.Draw(width, height, eye, up, center)
        
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