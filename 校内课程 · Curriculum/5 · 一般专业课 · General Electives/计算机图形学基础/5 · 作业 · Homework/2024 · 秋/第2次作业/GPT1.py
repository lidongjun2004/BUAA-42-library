import numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
import glm

# 顶点着色器
VERTEX_SHADER = """
#version 430
layout(location = 0) in vec4 position;
layout(location = 1) in vec2 texcoord;
layout(location = 2) in vec3 norm;

uniform mat4 MVP;
uniform mat4 Model; // 模型矩阵
uniform mat4 NormalMatrix; // 法线变换矩阵
uniform vec3 LightPos; // 光源位置
uniform vec3 LightColor; // 光源颜色

out vec2 fragTexcoord;
out vec3 fragAmbient;
out vec3 fragDiffuse;
out vec3 fragSpecular;

void main() {
    gl_Position = MVP * position;
    fragTexcoord = texcoord;

    // 光照计算
    vec3 norm = normalize(mat3(NormalMatrix) * norm);
    vec3 lightDir = normalize(vec3(LightPos - (Model * position).xyz));
    vec3 viewDir = normalize(-position.xyz);

    // 环境光
    float ambientStrength = 0.1;
    fragAmbient = ambientStrength * LightColor;

    // 漫反射光
    float diff = max(dot(norm, lightDir), 0.0);
    fragDiffuse = diff * LightColor;

    // 镜面反射光 (Blinn-Phong)
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(norm, halfwayDir), 0.0), 32.0); // 高光系数
    fragSpecular = spec * LightColor;
}
"""

# 片元着色器
FRAGMENT_SHADER = """
#version 430
in vec2 fragTexcoord;
in vec3 fragAmbient;
in vec3 fragDiffuse;
in vec3 fragSpecular;

uniform sampler2D texture0; // 纹理采样器
out vec4 fragColor;

void main() {
    vec3 texColor = texture(texture0, fragTexcoord).rgb;
    vec3 lighting = fragAmbient + fragDiffuse * texColor + fragSpecular;
    fragColor = vec4(lighting, 1.0);
}
"""

# 全局变量
shaderProgram = None
VAO = None
NumVertices = 0

def sphere_mesh():
    """生成球体的顶点、纹理坐标和法线。"""
    stacks, slices = 50, 50  # 经线和纬线数量
    vertices = []
    texcoords = []
    normals = []

    for i in range(stacks + 1):
        lat = np.pi * (-0.5 + float(i) / stacks)
        for j in range(slices + 1):
            lon = 2 * np.pi * float(j) / slices
            x = np.cos(lat) * np.cos(lon)
            y = np.sin(lat)
            z = np.cos(lat) * np.sin(lon)
            vertices.append([x, y, z, 1.0])
            texcoords.append([float(j) / slices, float(i) / stacks])
            normals.append([x, y, z])

    # 创建三角形面
    indices = []
    for i in range(stacks):
        for j in range(slices):
            p1 = i * (slices + 1) + j
            p2 = p1 + slices + 1
            indices.append([p1, p2, p1 + 1])
            indices.append([p2, p2 + 1, p1 + 1])

    vertices = np.array(vertices, np.float32)
    texcoords = np.array(texcoords, np.float32)
    normals = np.array(normals, np.float32)
    indices = np.array(indices, np.uint32).flatten()
    return vertices, texcoords, normals, indices

def initialize():
    """初始化 OpenGL 程序，包括着色器和缓冲对象。"""
    global shaderProgram, VAO, NumVertices

    # 编译着色器程序
    vertex_shader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragment_shader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    shaderProgram = shaders.compileProgram(vertex_shader, fragment_shader)

    # 生成球体网格
    vertices, texcoords, normals, indices = sphere_mesh()
    NumVertices = len(indices)

    # 创建 VAO 和 VBO
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes + texcoords.nbytes + normals.nbytes, None, GL_STATIC_DRAW)
    glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)
    glBufferSubData(GL_ARRAY_BUFFER, vertices.nbytes, texcoords.nbytes, texcoords)
    glBufferSubData(GL_ARRAY_BUFFER, vertices.nbytes + texcoords.nbytes, normals.nbytes, normals)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # 绑定顶点属性
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 16, None)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(vertices.nbytes))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(vertices.nbytes + texcoords.nbytes))
    glEnableVertexAttribArray(2)

    # 加载纹理
    texture = glGenTextures(1)
    image = np.array(Image.open('earthmap.jpg'))
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.shape[1], image.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    glGenerateMipmap(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

def render():
    """渲染场景，包括球体和光照计算。"""
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glUseProgram(shaderProgram)

    # 设置 MVP 矩阵
    proj = glm.perspective(glm.radians(60.0), 640 / 480, 0.1, 100.0)
    view = glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    model = glm.rotate(glm.mat4(1.0), glm.radians(30), glm.vec3(1, 0, 0))
    mvp = proj * view * model
    normal_matrix = glm.transpose(glm.inverse(model))

    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "MVP"), 1, GL_FALSE, glm.value_ptr(mvp))
    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "Model"), 1, GL_FALSE, glm.value_ptr(model))
    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "NormalMatrix"), 1, GL_FALSE, glm.value_ptr(normal_matrix))

    # 设置光源
    glUniform3f(glGetUniformLocation(shaderProgram, "LightPos"), 5.0, 5.0, 5.0)
    glUniform3f(glGetUniformLocation(shaderProgram, "LightColor"), 1.0, 1.0, 1.0)

    # 绑定纹理
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, 0)

    # 绘制
    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, NumVertices, GL_UNSIGNED_INT, None)
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutCreateWindow(b"Homework 2")
    initialize()
    glutDisplayFunc(render)
    glutMainLoop()

if __name__ == "__main__":
    main()
