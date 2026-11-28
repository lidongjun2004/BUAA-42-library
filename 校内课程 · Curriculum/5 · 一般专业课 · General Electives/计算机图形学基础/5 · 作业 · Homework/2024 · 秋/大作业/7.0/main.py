# 库函数引用
from OpenGL.GL import *
import os # 调整纹理文件路径分隔符,Win/Mac都可以使用
import time

# 自定义python程序引用
import Sphere
from AuxFunc import *
from Shader import *
from Data import PlanetDataOptimized, PlanetDataOriginal, GetViewSettings

#----------------------------------------------------------
# 相关参数设置
# 设置帧率
TARGET_FPS = 20
frame_interval = 1.0 / TARGET_FPS

# 透视投影矩阵参数
fov=60.0 #投影角
near=0.1 # 近平面
far=1e8 # 远平面

segments=100
#----------------------------------------------------------

state=int(input('''
请选择你要展示的内容:
0-太阳系原始比例;
1-太阳系优化比例;
2-地月系
''')) # 用户输入

if state==0 or state==1:
    # 初始化窗口和着色器程序
    str1='Solar System Original Scale'
    str2='Solar System Optimized Scale'
    
    # 光线参数
    LightPos = np.array([0.0, 0.0, 0.0], np.float32)      #设置光源位置
    LightColor = np.array([1.0, 1.0, 1.0], np.float32) #设置光源亮度

    # 设置对应模式下的观察位置参数
    MAX_RANGE=50000
    if state==1:
        MAX_RANGE=10000
    eye, center, up, OriLocation=GetViewSettings(MAX_RANGE)

    window, width, height=CreateWindow(str1 if state==0 else str2) #运行窗口默认大小正比于屏幕高(height)宽(width)比

    # 创建着色器
    PlanetShaderProgram=CreatePlanetShader(eye, center, up, LightPos, LightColor) # 行星着色器
    StarShaderProgram=CreateStarShader() # 恒星着色器
    shaderPrograms=[StarShaderProgram, PlanetShaderProgram]
    planets=[] # planets统一管理所有被渲染的行星       

    if state==0: # 原始比例太阳系
        Sun = Sphere.Globe('Sun', 6957.00, os.path.join('Pic', 'Sun.jpg'), StarShaderProgram, (0, 0, 0), 0, 25.38*24, 0)
        for name, data in PlanetDataOriginal.items():
            planets.append(Sphere.Globe(name, data[0], os.path.join('Pic', f"{name}.jpg"), PlanetShaderProgram, (0, (data[1]) ** 0.5/10, 0), data[2], data[3], data[4]))

    else: # 对应state==1,优化比例太阳系
        Sun = Sphere.Globe('Sun', 695.700, os.path.join('Pic', 'Sun.jpg'), StarShaderProgram, (0, 0, 0), 0, 25.38*24, 0)
        for name, data in PlanetDataOptimized.items():
            planets.append(Sphere.Globe(name, data[0], os.path.join('Pic', f"{name}.jpg"), PlanetShaderProgram, (0, (data[1]) ** 0.5/10, 0), data[2], data[3], data[4]))
    #----------------------------------------------------------
    
    #设置帧率,进行渲染
    last_time=glfw.get_time()

    while not glfw.window_should_close(window):
    
        # 自动更新窗口尺寸和展示内容比例
        width, height = glfw.get_framebuffer_size(window) # 获取窗口实际帧缓冲区尺寸
        glViewport(0, 0, width, height) # 更新视口大小
        FrameAdjust(fov, near, far, width, height, shaderPrograms) # 更新投影矩阵
        
        glfw.poll_events()

        eye, center, up = KeyboardControl(window, eye, center, up, OriLocation, width, height) # 实时更新视点信息

        # 控制帧率,渲染
        current_time = glfw.get_time()
        if current_time - last_time >= frame_interval:
            last_time=glfw.get_time()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            Sun.Draw(fov, near, far, width, height, eye, up, center)
            for planet in planets:
                planet.Draw(fov, near, far, width, height, eye, up, center)
            glfw.swap_buffers(window)
        
        # 降低CPU占用
        time.sleep(0.001)

    Terminate() # 结束运行,释放资源

elif state==2: # 优化比例的地月系
    str0='Earth System Optimized Scale'
    MAX_RANGE=500 # 设置观察参数
    eye, center, up, OriLocation=GetViewSettings(MAX_RANGE)

    # 光线参数
    LightRadius = 350 #设置光源位置
    LightColor = np.array([1.0, 1.0, 1.0], np.float32) #设置光源亮度

    window, width, height=CreateWindow(str0) #运行窗口大小正比于屏幕高(height)宽(width)比

    EarthShaderProgram=CreateEarthShader(LightRadius, LightColor) # 地球着色器程序
    shaderPrograms=[EarthShaderProgram]
    
    Earth=Sphere.Globe('Earth', 63.71, os.path.join('Pic', 'Earth.jpg'), EarthShaderProgram, (0, 0, 0), 365*60,60, 23.44)
    Moon=Sphere.Globe('Moon', 17.3814, os.path.join('Pic', 'Moon.jpg'), EarthShaderProgram, (128.13, 0, 0), 27.32*60, 27.32*60, 6.68)
    # 自转单位为日.将一天24h放大,乘以系数60,效果更好.
    # 二者具有相似的光线计算和数据搭载方式,因此都适用于EarthShaderProgram

    #设置帧率,进行渲染
    last_time=glfw.get_time()

    while not glfw.window_should_close(window):

        # 自动更新窗口尺寸和展示内容比例
        width, height = glfw.get_framebuffer_size(window) # 获取窗口实际帧缓冲区尺寸
        glViewport(0, 0, width, height) # 更新视口大小
        FrameAdjust(fov, near, far, width, height, shaderPrograms) # 更新投影矩阵
        glfw.poll_events()

        eye, center, up = KeyboardControl(window, eye, center, up, OriLocation, width, height) # 实时更新视点信息

        # 控制帧率,渲染
        current_time = glfw.get_time()
        if current_time - last_time >= frame_interval:
            last_time=glfw.get_time()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            Earth.Draw(fov, near, far, width, height, eye, up, center)
            Moon.Draw(fov, near, far, width, height, eye, up, center)
            
            glfw.swap_buffers(window)
        
        # 降低CPU占用
        time.sleep(0.001)

    Terminate() # 结束运行,释放资源

else:
    print('Wrong Input! Pleast Restart and Try Again.\n')