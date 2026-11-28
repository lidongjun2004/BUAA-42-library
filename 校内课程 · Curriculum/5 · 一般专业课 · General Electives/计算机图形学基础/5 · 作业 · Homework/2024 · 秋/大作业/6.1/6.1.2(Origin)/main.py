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

XEye=np.array([50000, 0, 0], np.float32)
XUp=np.array([0, 0, 1], np.float32)
XCenter=np.array([0, 0, 0], np.float32)

YEye=np.array([0, 50000, 0], np.float32)
YUp=np.array([0, 0, 1], np.float32)
YCenter=np.array([0, 0, 0], np.float32)

ZEye=np.array([0, 0, 50000], np.float32)
ZUp=np.array([1, 0, 0], np.float32)
ZCenter=np.array([0, 0, 0], np.float32)

OriLocation=[[XEye, XUp, XCenter], 
             [YEye, YUp, YCenter],
             [ZEye, ZUp, ZCenter]]
# 光线参数
LightPos = np.array([0.0, 0.0, 0.0], np.float32)      #设置光源位置
LightColor = np.array([1.0, 1.0, 1.0], np.float32) #设置光源亮度

Planet_data = {'Mercury':[24.40, 579100.00, 87.9693*24, 58.65*24],
               'Venus':[60.73, 1082089.30, 224.70*24, -243*24],
               'Earth':[63.78, 1496000.00, 365*24,24],
               'Mars':[67.94, 2279400.00, 686.98*24, 24.5],
               'Jupiter':[1429.84, 7783300.00, 4332.589*24, 10],
               'Saturn':[1193.00, 14270000.00, 10759.5*24, 10.6],
               'Uranus':[518.00, 28690000.00, 84.32*365*24, 17.25],
               'Neptune':[495.32, 45000000.00, 164.8*365*24, 16.1],
               }

#----------------------------------------------------------
# 初始化窗口和着色器程序
window, width, height=CreateWindow() #运行窗口大小正比于屏幕高(height)宽(width)比
PlanetShaderProgram=CreateShader(eye, center, up, LightPos, LightColor) # 行星着色器
StarShaderProgram=CreateStarShader() # 恒星着色器

#----------------------------------------------------------
# 初始化行星对象
Sun = Sphere.Planet('Sun', 6957.00, os.path.join('Pic', 'Sun.jpg'), StarShaderProgram, (0, 0, 0), 0, 0)
planets = []
k, c= 10, 1e7 # 调整轨道比例的参数
for name, data in Planet_data.items():
    planets.append(Sphere.Planet(name, data[0], os.path.join('Pic', f"{name}.jpg"), PlanetShaderProgram, (0, data[1], 0), data[2], data[3]))

#----------------------------------------------------------
#设置帧率,进行渲染
last_time=glfw.get_time()

while not glfw.window_should_close(window):
    # 高频检查键盘输入
    glfw.poll_events()
    
    eye, center, up = KeyboardControl(window, eye, center, up, OriLocation, width, height) # 更新此时的视角

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