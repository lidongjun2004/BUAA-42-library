# 库函数引用
from OpenGL.GL import *
from OpenGL.GL import shaders
import glfw
import glm
import math

# 自定义函数引用
from AuxFunc import *

def CreateWindow(name:str):
    global shaderProgram
    global window

    # 进行glfw初始化
    if not glfw.init():
        return

    # 设置画面大小(必须要先glfw.init())
    window_ratio=(math.pow(5, 0.5)-1)/2 # 黄金分割比
    mode = glfw.get_video_mode(glfw.get_primary_monitor()) # 获取显示器分辨率
    width, height=int(mode.size.width * window_ratio), int(mode.size.height * window_ratio)

    #设置版本号以及前向兼容,兼容Mac/Windows 
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

    window=glfw.create_window(width, height, name, None, None)
    if not window:
        glfw.terminate()
        SystemExit(-1)

    glfw.make_context_current(window)

    if glfw.make_context_current(window)==0:
        print("loading window error!\n")

    if not glfw.get_current_context():
        print("failed to get context")
        SystemExit(-1)
    
    return window, width, height

# --------------------------------------------------------------
# 行星着色器
PLANET_VERTEX_SHADER= """
#version 410 core

layout(location = 0) in vec4 position;
layout(location = 1) in vec2 texcoord;
layout(location = 2) in vec3 norm;

uniform mat4 MVP;
uniform mat4 M; // 模型变换矩阵
// uniform mat4 V; // 视图变换矩阵

out vec2 vt_texcoord;
out vec3 frag_position;
out vec3 frag_normal;

void main() {
    gl_Position = MVP * position; // 将位置转换到裁剪空间
    vt_texcoord = texcoord; // 传递纹理坐标

    // 计算世界空间中的顶点位置和法向量
    frag_position = vec3(M * position);
    frag_normal = mat3(transpose(inverse(M))) * norm;
}
"""

PLANET_FRAGMENT_SHADER = """
#version 410 core

uniform sampler2D tex0;
uniform vec3 lightPos; // 光源位置
uniform vec3 lightColor; // 光源颜色
uniform vec3 viewPos; // 相机位置

in vec2 vt_texcoord;
in vec3 frag_position;
in vec3 frag_normal;

out vec4 FragColor;

void main() {
    // 环境光
    float Ka = 0.01; // 环境光系数
    vec3 ambient = Ka * lightColor;

    // 漫反射
    vec3 norm = normalize(frag_normal);
    vec3 light_dir = normalize(lightPos - frag_position);
    float diff = max(dot(norm, light_dir), 0.0);
    vec3 diffuse = diff * lightColor+ 0.3;

    // 镜面反射
    vec3 view_dir = normalize(viewPos - frag_position);
    vec3 reflect_dir = reflect(-light_dir, norm);
    float spec = pow(max(dot(view_dir, reflect_dir), 0.0), 32.0); // 高光聚集程度
    float Ks = 0.2; // 镜面反射系数
    vec3 specular = Ks * spec * lightColor;

    // 获取纹理颜色
    vec3 kd = texture(tex0, vt_texcoord).rgb;

    // 组合光照
    vec3 color = ambient + kd * diffuse + specular;

    FragColor = vec4(color, 1.0);
}
"""


def CreatePlanetShader(eye, center, up, LightPos, LightColor): # 创建行星着色器
    # 创建着色器,VAO
    vertexshader = shaders.compileShader(PLANET_VERTEX_SHADER, GL_VERTEX_SHADER)
    fragmentshader = shaders.compileShader(PLANET_FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

    tempVAO = glGenVertexArrays(1)
    glBindVertexArray(tempVAO)

    shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)

    if not shaderProgram:
        print("Shader program compilation failed")
        SystemExit(-1)

    # 激活着色器程序
    glUseProgram(shaderProgram)

    # 设置光源、光照信息
    glUniform3f(glGetUniformLocation(shaderProgram, "lightPos"), LightPos[0], LightPos[1], LightPos[2])
    glUniform3f(glGetUniformLocation(shaderProgram, "lightColor"), LightColor[0], LightColor[1], LightColor[2])

    # 设置相机位置
    glUniform3f(glGetUniformLocation(shaderProgram, "viewPos"), glm.vec3(eye).x, glm.vec3(eye).y, glm.vec3(eye).z)

    # # 设置视图矩阵
    # view = glm.lookAt(glm.vec3(eye), glm.vec3(center), glm.vec3(up))  # 调整此处视图矩阵
    # view_loc = glGetUniformLocation(shaderProgram, "V")
    # glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))

    # 设置清除色,开启深度测试
    glClearColor(0, 0, 0, 1)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)

    return shaderProgram

# --------------------------------------------------------------
# 恒星着色器
STAR_VERTEX_SHADER='''
#version 410 core
 
    layout(location = 0) in vec4 position;
    layout(location = 1) in vec2 texcoord;

    uniform mat4 MVP;
    uniform mat4 M; //法线变换矩阵

    out vec2 vt_texcoord;

    void main() {
        gl_Position = MVP * position;
        vt_texcoord=texcoord;
    } 
'''


STAR_FRAGMENT_SHADER='''
#version 410 core
    uniform sampler2D tex0;

    in vec2 vt_texcoord;
    out vec4 FragColor;
    void main() {
        FragColor = texture(tex0, vt_texcoord);
    }
'''


def CreateStarShader():  # 创建恒星着色器
    # 创建着色器,VAO
    vertexshader = shaders.compileShader(STAR_VERTEX_SHADER, GL_VERTEX_SHADER)
    fragmentshader = shaders.compileShader(STAR_FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    
    tempVAO = glGenVertexArrays(1)
    glBindVertexArray(tempVAO)

    shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)

    if not shaderProgram:
        print("Shader program compilation failed")
        SystemExit(-1)

    # 激活着色器程序
    glUseProgram(shaderProgram)
    # ----------------------------------------------

    # 设置清除色,开启深度测试
    glClearColor(0, 0, 0, 1)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)

    return shaderProgram

# --------------------------------------------------------------
# 地球着色器
EARTH_VERTEX_SHADER='''
    #version 410 core

    layout(location = 0) in vec4 position;
    layout(location = 1) in vec2 texcoord;
    layout(location = 2) in vec3 norm; // 法线

    uniform mat4 MVP; // 投影-视图-模型矩阵
    uniform mat4 M;   // 模型矩阵

    out vec2 vt_texcoord;
    out vec3 frag_normal;   // 传递法线
    out vec3 frag_position; // 传递片段位置（世界空间）

    void main() {
        gl_Position = MVP * position;
        vt_texcoord = texcoord;
        frag_position = vec3(M * position);  // 计算片段的世界坐标
        frag_normal = mat3(transpose(inverse(M))) * norm; // 变换法线到世界空间
    }
'''


EARTH_FRAGMENT_SHADER='''
    #version 410 core

    uniform sampler2D tex0;
    uniform vec3 lightDir;           // 平行光方向（世界空间）
    uniform vec3 lightColor;         // 光源颜色
    uniform float ambientStrength;   // 环境光强度

    in vec2 vt_texcoord;
    in vec3 frag_normal;   // 接收插值后的法线
    in vec3 frag_position; // 接收片段位置

    out vec4 FragColor;

    void main() {
        // 环境光
        vec3 ambient = ambientStrength * lightColor;

        // 漫反射光照
        vec3 norm = normalize(frag_normal);      // 归一化法线
        vec3 dirLight = normalize(-lightDir);   // 平行光方向取反
        float diff = max(dot(norm, dirLight), 0.0);
        vec3 diffuse = diff * lightColor;

        // 组合光照
        vec3 finalColor = (ambient + diffuse) * texture(tex0, vt_texcoord).rgb;

        FragColor = vec4(finalColor, 1.0);
    }
'''


def CreateEarthShader(LightRadius, LightColor): # 创建地球着色器
    vertexshader = shaders.compileShader(EARTH_VERTEX_SHADER, GL_VERTEX_SHADER)
    fragmentshader = shaders.compileShader(EARTH_FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    
    tempVAO = glGenVertexArrays(1)
    glBindVertexArray(tempVAO)

    ShaderProgram = shaders.compileProgram(vertexshader, fragmentshader)

    if not ShaderProgram:
        print("Shader program compilation failed")
        SystemExit(-1)

    # 激活着色器程序
    glUseProgram(ShaderProgram)
    # ----------------------------------------------

    # 设置清除色,开启深度测试
    glClearColor(0, 0, 0, 1)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)

    # 光线参数
    light_direction = np.array([0, -LightRadius, 0.0], np.float32)      #设置光源位置
    light_color = np.array(LightColor, np.float32) #设置光源亮度
    ambient_strength=0.3

    # 设置光照方向、颜色和环境光强度
    light_dir_loc = glGetUniformLocation(ShaderProgram, "lightDir")
    light_color_loc = glGetUniformLocation(ShaderProgram, "lightColor")
    ambient_strength_loc = glGetUniformLocation(ShaderProgram, "ambientStrength")

    glUniform3fv(light_dir_loc, 1, light_direction)
    glUniform3fv(light_color_loc, 1, light_color)
    glUniform1f(ambient_strength_loc, ambient_strength)

    return ShaderProgram