import numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.GL import shaders
import glfw
import glm 
from AuxFunc import *

# 相机参数
eye=np.array([10, 0, 0], np.float32)
center=np.array([0, 0, 0], np.float32)
up=np.array([0, 0, 1], np.float32)

# 光线参数
lightPos = np.array([10, 0.0, 0.0], np.float32)      #设置光源位置
lightColor = np.array([50.0, 50.0, 50.0], np.float32) #设置光源亮度

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
        float shininess=1.0;  // 高光聚集程度
        float spec=pow(max(dot(norm, halfwaydir), 0.0), shininess);
        float Ks=0.001; // 控制高光亮度
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
    
def CreateWindow():
    global shaderProgram
    global window

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
        SystemExit(-1)

    glfw.make_context_current(window)

    if glfw.make_context_current(window)==0:
        print("loading window error!\n")

    if not glfw.get_current_context():
        print("failed to get context")
        SystemExit(-1)
    
    return window
    
def CreateShader():
    # 创建着色器,VAO
    vertexshader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragmentshader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    
    tempVAO = glGenVertexArrays(1)
    glBindVertexArray(tempVAO)

    shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)

    if not shaderProgram:
        print("Shader program compilation failed")
        SystemExit(-1)

    # 激活着色器程序
    glUseProgram(shaderProgram)
    # ----------------------------------------------

    # 设置光源、光照信息
    glUniform3f(glGetUniformLocation(shaderProgram,"lightPos"), lightPos[0], lightPos[1], lightPos[2])
    glUniform3f(glGetUniformLocation(shaderProgram,"lightColor"), lightColor[0], lightColor[1], lightColor[2])

    # 设置相机位置
    glUniform3f(glGetUniformLocation(shaderProgram, "viewPos"), glm.vec3(eye).x, glm.vec3(eye).y, glm.vec3(eye).z)

    # 设置清除色,开启深度测试
    glClearColor(0, 0, 0, 1)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)

    return shaderProgram
    # ---------------------------------------------
