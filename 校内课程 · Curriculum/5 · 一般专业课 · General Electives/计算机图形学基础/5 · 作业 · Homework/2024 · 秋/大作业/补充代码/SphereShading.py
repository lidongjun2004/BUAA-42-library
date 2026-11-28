import numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.GL import shaders
import glfw
import glm 
import time

# 对应任务三:实现Blinn-Phong模型
'''
程序亮点：
1. 参数全部设置在前面，方便调整。参数包括：画面大小（画幅）、球的粒度、相机参数、光照参数、帧率参数
2. 
'''

# 画面长宽
width=800
height=600

# 生成球的粒度
SphereSlice=40
NumVertex=(SphereSlice+1)*(SphereSlice+1)
NumIndex=6*SphereSlice*SphereSlice

# 相机参数
eye=np.array([5, 0, 0], np.float32)
center=np.array([0, 0, 0], np.float32)
up=np.array([0, 0, 1], np.float32)

# 光线参数
lightPos = np.array([3.5, 0.0, 0.0], np.float32)      #设置光源位置
lightColor = np.array([8.0, 8.0, 8.0], np.float32) #设置光源亮度

# 设置帧率
TARGET_FPS = 10
frame_interval = 1.0 / TARGET_FPS

VERTEX_SHADER = """
#version 410 core
 
    layout(location = 0) in vec4 position;
    layout(location = 1) in vec2 texcoord;
    layout(location = 2) in vec3 norm;

    uniform mat4 MVP;
    uniform mat4 M; //法线变换矩阵
    uniform vec3 lightPos; //光源在世界坐标下的位置
    uniform vec3 lightColor; //光源的颜色
    uniform vec3 viewPos; // 相机位置

    out vec2 vt_texcoord;
    out vec3 ambient;
    out vec3 diffuse;
    out vec3 specular;

    void main() {
        gl_Position = MVP * position;
        vt_texcoord=texcoord;
        //环境光
        float Ka = 0.01; // 环境光系数
        ambient = Ka * lightColor;

        //漫反射
        vec3 norm = normalize(mat3(transpose(inverse(M))) * norm);
        vec3 dd = lightPos - (M*position).xyz;
        vec3 lightdir = normalize(dd);
        float r2 = dot(dd, dd);
        diffuse = lightColor/r2 * max(dot(norm, lightdir), 0.0);

        //镜面反射
        vec3 viewdir=normalize(viewPos-dd);  // 观察方向
        vec3 halfwaydir=normalize(lightdir+viewdir);    // 半程向量
        float shininess=16.0;  // 高光聚集程度
        float spec=pow(max(dot(norm, halfwaydir), 0.0), shininess);
        float Ks=0.2; // 控制高光亮度
        specular=Ks*lightColor*spec;  // 镜面反射光
    } 
"""

FRAGMENT_SHADER = """
#version 410 core
    uniform sampler2D tex0;

    in vec3 ambient;
    in vec3 diffuse;
    in vec3 specular;
    in vec2 vt_texcoord;
    out vec4 FragColor;
    void main() {
        
        vec3 kd = texture(tex0, vt_texcoord).rgb; // 漫反射系数
        vec3 color = ambient + kd*diffuse + specular; 
        FragColor = vec4(color, 1.0);
    }
"""

shaderProgram = None
VAO = None
Num_T = 0
time_count = 0

def InitSphere(): # 创建球, 默认球心在原点
    global shaderProgram
    global VERTEX_SHADER
    global FRAGMENT_SHADER

    # 生成并计算顶点索引列表, 坐标列表,纹理坐标列表和法向量列表
    indexList=np.zeros((NumIndex, ), np.uint32)
    pointList=np.zeros((NumVertex, 4), np.float32)
    texList=np.zeros((NumVertex, 2), np.float32)
    normList=np.zeros((NumVertex, 3), np.float32)

    x, y, z, u, v=0.0, 0.0, 0.0, 0.0, 0.0
    for i in range(SphereSlice+1):
        for j in range(SphereSlice+1):
            x=np.sin(np.radians(180*i/SphereSlice))*np.cos(np.radians(360*j/SphereSlice))
            y=np.sin(np.radians(180*i/SphereSlice))*np.sin(np.radians(360*j/SphereSlice))
            z=-np.cos(np.radians(180*i/SphereSlice))
            u=1.0*j/SphereSlice  # 经度映射到水平纹理坐标
            v=1.0-1.0*i/SphereSlice  # 纬度映射到垂直纹理坐标
            texList[i*(SphereSlice+1)+j]=np.array([u, v], np.float32)
            pointList[i*(SphereSlice+1)+j]=np.array([x, y, z, 1.0], np.float32)
            normList[i*(SphereSlice+1)+j]=np.array([x, y, z], np.float32)

    for i in range(SphereSlice):
        for j in range(SphereSlice):
            indexList[6*(i*SphereSlice+j)+0]=i*(SphereSlice+1)+j
            indexList[6*(i*SphereSlice+j)+1]=i*(SphereSlice+1)+j+1
            indexList[6*(i*SphereSlice+j)+2]=(i+1)*(SphereSlice+1)+j
            indexList[6*(i*SphereSlice+j)+3]=i*(SphereSlice+1)+j+1
            indexList[6*(i*SphereSlice+j)+4]=(i+1)*(SphereSlice+1)+j+1
            indexList[6*(i*SphereSlice+j)+5]=(i+1)*(SphereSlice+1)+j

    return indexList, pointList, texList, normList

def calc_and_update_mvp(width, height):
    global time_count
    global shaderProgram
    time_count=glfw.get_time()* 50
    
    proj = glm.perspective(glm.radians(60.0),float(width)/float(height),0.1,20.0)
    view = glm.lookAt(glm.vec3(eye), glm.vec3(center),glm.vec3(up))
    model =  glm.mat4(1.0)
    theta=np.radians(66.5)
    model = glm.rotate(model, glm.radians(time_count * 0.5), glm.vec3(0, np.cos(theta), np.sin(theta)))
    mvp = proj * view * model

    mvp_loc = glGetUniformLocation(shaderProgram,"MVP")
    m_loc = glGetUniformLocation(shaderProgram, "M")

    glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, glm.value_ptr(mvp))
    glUniformMatrix4fv(m_loc, 1, GL_FALSE, glm.value_ptr(model))


def main():
    global shaderProgram

    # 进行glfw初始化
    if not glfw.init():
        return
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

    window=glfw.create_window(800,600, "SphereShading_withBlinnPhongModel", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    if glfw.make_context_current(window)==0:
        print("loading window error!\n")
    
    if not glfw.get_current_context():
        print("failed to get context")
        return
    
    check_gl_error()

    # 创建着色器,VAO, VBO
    vertexshader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragmentshader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    
    shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)
    if shaderProgram==0:
        print('fail to compile shader!')
        return
    
    

    # 创建一个球,并且在VBO上绑定数据
    indexList, point, tex, norm=[], [], [], []
    indexList, point, tex, norm=InitSphere()

    pointList, normList, texList=[], [], []
    
    for i in range(NumIndex):
        pointList.append(point[indexList[i]])
        texList.append(tex[indexList[i]])
        normList.append(norm[indexList[i]])
    
    pointList=np.array(pointList, np.float32)
    texList=np.array(texList, np.float32)
    normList=np.array(normList, np.float32)
    
    # 绑定顶点坐标
    VBO1= glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO1)
    glBufferData(GL_ARRAY_BUFFER, pointList.nbytes, pointList, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4*4, None)
    glEnableVertexAttribArray(0)

    # 绑定纹理坐标
    VBO2=glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO2)
    glBufferData(GL_ARRAY_BUFFER, texList.nbytes, texList, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4*2, None)
    glEnableVertexAttribArray(1)

    '''shader中关于纹理的部分,需要搞懂'''

    # 绑定法向量
    VBO3=glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO3)
    glBufferData(GL_ARRAY_BUFFER, normList.nbytes, normList, GL_STATIC_DRAW)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 4*3, None)
    glEnableVertexAttribArray(2)

    # 设置清除色,开启深度测试
    glClearColor(0, 0, 0, 1)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    # glEnable(GL_CULL_FACE)

    # 激活着色器程序
    glUseProgram(shaderProgram)
    
    # 绑定纹理
    tex = glGenTextures(1)
    img = np.array(Image.open('earthmap.jpg'))
    
    if img.size==0:
        print("fail to load image!")
        return
    
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.shape[1], img.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, img)
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
    glGenerateMipmap(GL_TEXTURE_2D)
  
    glUniform1i(glGetUniformLocation(shaderProgram, "tex0"), 0)
    
    # 设置光源、光照信息
    glUniform3f(glGetUniformLocation(shaderProgram,"lightPos"), lightPos[0], lightPos[1], lightPos[2])
    glUniform3f(glGetUniformLocation(shaderProgram,"lightColor"), lightColor[0], lightColor[1], lightColor[2])

    # 设置相机位置
    glUniform3f(glGetUniformLocation(shaderProgram, "viewPos"), glm.vec3(eye).x, glm.vec3(eye).y, glm.vec3(eye).z)

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
            calc_and_update_mvp(width, height)
            glDrawArrays(GL_TRIANGLES, 0, NumIndex) 
            glfw.swap_buffers(window)
        
        # 降低CPU占用
        time.sleep(0.001)

    # 进行解绑,并终止程序
    glUseProgram(0) # 禁用当前激活的着色器程序
    glBindTexture(GL_TEXTURE_2D, 0) # 解绑纹理
    
    glBindVertexArray(0) # 解绑VAO
    glBindBuffer(GL_ARRAY_BUFFER, 0) # 解绑VBO
    glfw.terminate()

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


if __name__=="__main__":
    main()
