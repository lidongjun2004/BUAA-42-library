import numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
import glm  # pip install PyGLM

# 顶点着色器
VERTEX_SHADER = """
#version 430
layout(location = 0) in vec4 position;
layout(location = 1) in vec2 texcoord;
layout(location = 2) in vec3 norm;

uniform mat4 MVP;
uniform mat4 M;
uniform vec3 lightPos;

out vec2 vt_texcoord;
out vec3 fragPos;
out vec3 fragNormal;

void main() {
    gl_Position = MVP * position;

    // 传递纹理坐标
    vt_texcoord = texcoord;

    // 计算片元位置（世界坐标系）
    fragPos = (M * position).xyz;
    fragNormal = mat3(M) * norm;
}
"""

# 片元着色器
FRAGMENT_SHADER = """
#version 430
uniform sampler2D tex0;
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;

in vec2 vt_texcoord;
in vec3 fragPos;
in vec3 fragNormal;

out vec4 fragColor;

// 简单的 Blinn-Phong 光照计算
vec3 blinn_phong(vec3 position, vec3 normal) {
    vec3 ambient = 0.1 * lightColor;

    // 光照方向
    vec3 lightDir = normalize(lightPos - position);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    // 镜面反射
    vec3 viewDir = normalize(viewPos - position);
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), 32.0);
    vec3 specular = spec * lightColor;

    return ambient + diffuse + specular;
}

// 阴影计算函数
float shadowCalculation(vec3 fragPos, vec3 lightPos, vec3 planeNormal) {
    vec3 toLight = normalize(lightPos - fragPos);
    float dotProduct = max(dot(planeNormal, toLight), 0.0);
    return dotProduct;
}

void main() {
    // 计算光照
    vec3 normal = normalize(fragNormal);
    vec3 lighting = blinn_phong(fragPos, normal);

    // 获取漫反射颜色
    vec3 kd = texture(tex0, vt_texcoord).rgb;

    // 计算阴影
    float shadow = shadowCalculation(fragPos, lightPos, vec3(0.0, 1.0, 0.0));  // 阴影投射到水平面

    // 最终颜色（考虑阴影）
    vec3 color = lighting * kd * shadow;

    fragColor = vec4(color, 1.0);
}
"""

shaderProgram = None
VAO = None
Num_T = 0
time_count = 0

# 创建球体的网格
def sphere_mesh(stacks=50, slices=50):
    vertices = []
    texcoords = []
    normals = []
    indices = []

    for i in range(stacks + 1):
        phi = np.pi * (-0.5 + float(i) / stacks)
        for j in range(slices + 1):
            theta = 2 * np.pi * float(j) / slices
            x = np.cos(phi) * np.cos(theta)
            y = np.sin(phi)
            z = np.cos(phi) * np.sin(theta)
            u = float(j) / slices
            v = float(i) / stacks

            vertices.append([x, y, z, 1.0])
            texcoords.append([u, v])
            normals.append([x, y, z])

    for i in range(stacks):
        for j in range(slices):
            p1 = i * (slices + 1) + j
            p2 = p1 + slices + 1
            indices.append([p1, p2, p1 + 1])
            indices.append([p2, p2 + 1, p1 + 1])

    vertices = np.array(vertices, dtype=np.float32)
    texcoords = np.array(texcoords, dtype=np.float32)
    normals = np.array(normals, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

    return vertices, texcoords, normals, indices.reshape(-1)

# 创建平面网格
def plane_mesh():
    vertices = [
        [-10.0, -1.0, 10.0, 1.0], [0.0, 0.0], [0.0, 1.0, 0.0],
        [10.0, -1.0, 10.0, 1.0], [1.0, 0.0], [0.0, 1.0, 0.0],
        [10.0, -1.0, -10.0, 1.0], [1.0, 1.0], [0.0, 1.0, 0.0],
        [-10.0, -1.0, -10.0, 1.0], [0.0, 1.0], [0.0, 1.0, 0.0]
    ]

    indices = [0, 1, 2, 0, 2, 3]  # 形成两个三角形

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)


def initialize():
    global shaderProgram, VAO, Num_T, planeVAO, planeNum_T

    vertexshader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragmentshader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)

    # 创建球体网格
    vertices, texcoords, normals, indices = sphere_mesh()
    Num_T = indices.shape[0]

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(3)
    glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 16, None)
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
    glBufferData(GL_ARRAY_BUFFER, texcoords.nbytes, texcoords, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 8, None)
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
    glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 12, None)
    glEnableVertexAttribArray(2)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # 加载漫反射贴图
    tex = glGenTextures(1)
    img = np.array(Image.open("earthmap.jpg").convert("RGB"))
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.shape[1], img.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, img)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glGenerateMipmap(GL_TEXTURE_2D)

    # 创建平面网格
    planeVertices, planeIndices = plane_mesh()
    planeNum_T = planeIndices.shape[0]

    planeVAO = glGenVertexArrays(1)
    glBindVertexArray(planeVAO)

    planeVBO = glGenBuffers(3)
    glBindBuffer(GL_ARRAY_BUFFER, planeVBO[0])
    glBufferData(GL_ARRAY_BUFFER, planeVertices.nbytes, planeVertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 16, None)
    glEnableVertexAttribArray(0)

    planeEBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, planeEBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, planeIndices.nbytes, planeIndices, GL_STATIC_DRAW)


def calc_mvp(width, height):
    proj = glm.perspective(glm.radians(60.0), float(width) / float(height), 0.1, 20.0)
    view = glm.lookAt(glm.vec3(0.0, 0.0, 3.0), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    model = glm.rotate(glm.mat4(1.0), glm.radians(time_count * 5), glm.vec3(1, 1, 0))
    return model, proj * view * model


def render():
    global shaderProgram, VAO, Num_T, planeVAO, planeNum_T

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glEnable(GL_DEPTH_TEST)

    glUseProgram(shaderProgram)

    mvp_loc = glGetUniformLocation(shaderProgram, "MVP")
    m_loc = glGetUniformLocation(shaderProgram, "M")
    shadingMode_loc = glGetUniformLocation(shaderProgram, "shadingMode")

    m_mat, mvp_mat = calc_mvp(640, 480)
    glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, glm.value_ptr(mvp_mat))
    glUniformMatrix4fv(m_loc, 1, GL_FALSE, glm.value_ptr(m_mat))

    lightPos = np.array([3.0, 3.0, 3.0], np.float32)
    viewPos = np.array([0.0, 0.0, 3.0], np.float32)
    lightColor = np.array([3.0, 3.0, 3.0], np.float32)

    glUniform3f(glGetUniformLocation(shaderProgram, "lightPos"), *lightPos)
    glUniform3f(glGetUniformLocation(shaderProgram, "viewPos"), *viewPos)
    glUniform3f(glGetUniformLocation(shaderProgram, "lightColor"), *lightColor)

    # 设置不同的采样频率（0: 三角形级别, 1: 顶点级别, 2: 像素级别）
    glUniform1i(shadingMode_loc, 1)

    glActiveTexture(GL_TEXTURE0)
    glUniform1i(glGetUniformLocation(shaderProgram, "tex0"), 0)

    # 绘制平面
    glBindVertexArray(planeVAO)
    glDrawElements(GL_TRIANGLES, planeNum_T, GL_UNSIGNED_INT, None)

    # 绘制球体
    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, Num_T, GL_UNSIGNED_INT, None)

    glutSwapBuffers()


def animate(value):
    global time_count

    glutPostRedisplay()
    glutTimerFunc(200, animate, 0)

    time_count += 1.0


def main():
    glutInit([])
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutCreateWindow(b"Blinn-Phong Lighting with Shadow")
    initialize()
    glutDisplayFunc(render)
    glutTimerFunc(200, animate, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()
