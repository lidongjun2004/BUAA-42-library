import numpy as np
from PIL import Image 
from OpenGL.GL import *
from OpenGL.GL import shaders
import glfw
import glm 
import time

'''
这个是在ShadingFinal.py的基础上修改的.
相比于ShadingFinal.py,对函数的整体架构进行了重构.如下1:
函数执行时,main()函数调用initialize()和display().
initialize()函数完成了编译着色器,创建窗口,VAO,VBO等操作.
display则是对应glfw主循环,是程序运行展示结果的地方.
'''

# 画面长宽
width=800
height=600

# 光照位置信息
lightPos = np.array([3.0, 0.0, 0.0], np.float32)      #设置光源位置
lightColor = np.array([10.0, 10.0, 10.0], np.float32) #设置光源亮度

# 相机参数信息
eye=np.array([3.0, 0.0, 0.0],np.float32)
center=np.array([0,0,0], np.float32)
up=np.array([0,0,1], np.float32)

# 设置帧率
TARGET_FPS = 30
frame_interval = 1.0 / TARGET_FPS

Num_T = 0
time_count = 0

VERTEX_SHADER = """
#version 410 core
 
    layout(location = 0) in vec4 position;
    layout(location = 1) in vec2 texcoord;
    layout(location = 2) in vec3 norm;

    uniform mat4 MVP;
    uniform mat4 M; //法线变换矩阵
    uniform vec3 lightPos; //光源在世界坐标下的位置
    uniform vec3 lightColor; //光源的颜色

    out vec2 vt_texcoord;
    out vec3 ambient;
    out vec3 diffuse;

    void main() {
        gl_Position = MVP * position;
        
        //环境光
        float ambientStrength = 0.01;
        ambient = ambientStrength * lightColor;

        //漫反射
        vec3 norm = normalize(mat3(M) * norm);
        vec3 dd = lightPos - (M*position).xyz;
        vec3 lightdir = normalize(dd);
        float r2 = dot(dd, dd);
        diffuse = lightColor/r2 * max(dot(norm, lightdir), 0.0);

        vt_texcoord = texcoord;
    } 
"""

FRAGMENT_SHADER = """
#version 410 core
    uniform sampler2D tex0;

    in vec3 ambient;
    in vec3 diffuse;
    in vec2 vt_texcoord;
    out vec4 FragColor;
    void main() {
        
        vec3 kd = texture(tex0, vt_texcoord).rgb;
        vec3 color = ambient + kd*diffuse; 
        FragColor = vec4(color, 1.0);
 
    }

"""


def cube(): #六面体
    pointList = [[-0.5, -0.5,  0.5, 1.0 ],
                [-0.5,  0.5,  0.5, 1.0 ],
                [0.5,  0.5,  0.5, 1.0 ],
                [0.5, -0.5,  0.5, 1.],
                [-0.5, -0.5, -0.5, 1.0 ],
                [-0.5,  0.5, -0.5, 1.0 ],
                [0.5,  0.5, -0.5, 1.0 ],
                [0.5, -0.5, -0.5, 1.0 ]]

    indexList = [   [0, 2, 1],
                    [0, 3, 2], #front

                    [3, 6, 2],
                    [3, 7, 6], #right

                    [7, 5, 6],
                    [7, 4, 5], #back

                    [4, 1, 5],
                    [4, 0, 1], #left

                    [1, 6, 5],
                    [1, 2, 6], #top

                    [0, 7, 4],
                    [0, 3, 7]]  #bottom
    
    Norm_Vs = [     [0, 0, 1], #front
                    [1, 0, 0], #right
                    [0, 0, -1], #back
                    [-1, 0, 0], #left
                    [0, 1, 0], #top
                    [0, -1, 0]] #bottom
    
    points, norms, texcoords = [], [], []
    for i in range(6):
        points.append(pointList[indexList[2*i][0]])
        points.append(pointList[indexList[2*i][1]])
        points.append(pointList[indexList[2*i][2]])
        texcoords.append([0, 0])
        texcoords.append([1, 1])
        texcoords.append([0, 1])
        norms.append(Norm_Vs[i])
        norms.append(Norm_Vs[i])
        norms.append(Norm_Vs[i])

        points.append(pointList[indexList[2*i+1][0]])
        points.append(pointList[indexList[2*i+1][1]])
        points.append(pointList[indexList[2*i+1][2]])
        texcoords.append([0, 0])
        texcoords.append([1, 0])
        texcoords.append([1, 1])
        norms.append(Norm_Vs[i])
        norms.append(Norm_Vs[i])
        norms.append(Norm_Vs[i])
    
    return np.array(points, np.float32), np.array(texcoords, np.float32), np.array(norms, np.float32)


def calc_and_update_mvp(width, height):
    global time_count

    time_count=glfw.get_time()*50
    proj = glm.perspective(glm.radians(60.0),float(width)/float(height),0.1,20.0)
    view = glm.lookAt(glm.vec3(eye), glm.vec3(center),glm.vec3(up))
    
    model =  glm.mat4(1.0)
    model = glm.rotate(model, glm.radians(time_count * 0.5), glm.vec3(0, 1, 1))
    
    mvp = proj * view * model
    
    mvp_loc = glGetUniformLocation(shaderProgram,"MVP")
    m_loc = glGetUniformLocation(shaderProgram, "M")

    glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, glm.value_ptr(mvp))
    glUniformMatrix4fv(m_loc, 1, GL_FALSE, glm.value_ptr(model))


def initialize():
    global time_count
    global Num_T
    global shaderProgram
    global window
    #初始化窗口
    if not glfw.init():
        print('fail to initialize window!\n')
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

    window=glfw.create_window(800,600, "shading with GLFW", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.make_context_current(window)

    # 链接顶点/面元着色器,创建VAO,链接着色器程序,给VBO搭载数据（前两步顺序不能错！）
    vertexshader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragmentshader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)
    if shaderProgram==0:
        print('fail to compile shader!\n')
        return
    
    glUseProgram(shaderProgram)

    '''
    Shader Program验证机制：
    在OpenGL 4.x中,着色器程序在调用glValidateProgram时会对当前的上下文状态进行检查.
    例如,glValidateProgram会尝试验证与顶点属性（如位置,法线,纹理坐标）相关的内容.
    如果未绑定任何VAO或VBO,着色器程序会因为“未绑定顶点数组对象”而失败.
    因此要在shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)之前创建VAO
    '''
    
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    
    # 绑定顶点坐标,纹理,法线信息
    points, texcoords, norms = cube()
    Num_T = points.shape[0]
    glBufferData(GL_ARRAY_BUFFER, points.nbytes+texcoords.nbytes+norms.nbytes, None, GL_STATIC_DRAW)
    glBufferSubData(GL_ARRAY_BUFFER, 0, points.nbytes, points)
    glBufferSubData(GL_ARRAY_BUFFER, points.nbytes, texcoords.nbytes, texcoords)
    glBufferSubData(GL_ARRAY_BUFFER, points.nbytes+texcoords.nbytes, norms.nbytes, norms)

    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4*4, None)
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 2*4, ctypes.c_void_p(points.nbytes))
    glEnableVertexAttribArray(1)

    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 3*4, ctypes.c_void_p(points.nbytes+texcoords.nbytes))
    glEnableVertexAttribArray(2)

    # 激活纹理
    tex = glGenTextures(1)
    img = np.array(Image.open('Pic/chessboard.jpg'))

    if img.size==0:
        print('load image failed!')
        return -1

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.shape[1], img.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, img)
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
    glGenerateMipmap(GL_TEXTURE_2D)

    glUniform1i(glGetUniformLocation(shaderProgram, "tex0"), 0)

    # 设置背景清除色,开启深度测试,绑定光源信息
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)

    glUniform3f(glGetUniformLocation(shaderProgram,"lightPos"),
                lightPos[0], lightPos[1], lightPos[2])
    glUniform3f(glGetUniformLocation(shaderProgram,"lightColor"),
                lightColor[0], lightColor[1], lightColor[2])
    

def display():
    # 设置帧率控制进行渲染
    last_time=glfw.get_time()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        check_keyboard(window)
        
        # 控制帧率
        current_time = glfw.get_time()
        if current_time - last_time >= frame_interval:
            last_time=glfw.get_time()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            calc_and_update_mvp(width, height)
            glDrawArrays(GL_TRIANGLES, 0, Num_T) 
            glfw.swap_buffers(window)
        
        # 降低CPU占用
        time.sleep(0.001)

    # 释放占用资源
    glUseProgram(0)
    glBindTexture(GL_TEXTURE_2D, 0)
    glBindVertexArray(0)
    glfw.terminate()


def main(): # 主函数
    initialize() # 初始化
    display() # 展示渲染结果


def check_keyboard(window):
    # 按下ESC键则终止程序
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def framebuffer_size_callback(window, width:int, height:int):
    # 自动调整画布大小
    glViewport(0, 0, width, height);

if __name__ == '__main__':
    main()