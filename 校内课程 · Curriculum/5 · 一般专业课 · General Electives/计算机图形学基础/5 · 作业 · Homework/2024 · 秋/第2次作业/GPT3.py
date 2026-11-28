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
uniform mat4 Model;
uniform mat3 NormalMatrix;
uniform vec3 LightPos;
uniform vec3 LightColor;

out vec2 fragTexcoord;
out vec3 fragAmbient;
out vec3 fragDiffuse;
out vec3 fragSpecular;
out mat3 TBN;  // TBN 矩阵传递到片元着色器

void main() {
    gl_Position = MVP * position;
    fragTexcoord = texcoord;

    vec3 normal = normalize(NormalMatrix * norm);
    vec3 tangent = normalize(vec3(1.0, 0.0, 0.0));  // 假设切线方向
    vec3 bitangent = cross(normal, tangent);
    TBN = mat3(tangent, bitangent, normal);

    vec3 lightDir = normalize(LightPos - vec3(Model * position));
    vec3 viewDir = normalize(-vec3(Model * position));

    // 环境光
    float ambientStrength = 0.1;
    fragAmbient = ambientStrength * LightColor;

    // 漫反射
    float diff = max(dot(normal, lightDir), 0.0);
    fragDiffuse = diff * LightColor;

    // 镜面反射 (Blinn-Phong)
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), 32.0);
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
in mat3 TBN;  // 从顶点着色器传来的 TBN 矩阵

uniform sampler2D normalMap;      // 法线贴图

uniform sampler2D texture0;
out vec4 fragColor;

void main() {
    // 使用纹理采样颜色，优化 LOD
    vec3 texColor = textureLod(texture0, fragTexcoord, 0.0).rgb;
    // 从法线贴图获取扰动的法线（从 [0, 1] 转换为 [-1, 1]）
    vec3 normal = texture(normalMap, fragTexcoord).rgb;
    normal = normalize(normal * 2.0 - 1.0);  // 转换为切线空间法线

    // 将切线空间法线转换为世界空间
    vec3 worldNormal = normalize(TBN * normal);
    vec3 lighting = fragAmbient + fragDiffuse * texColor + fragSpecular;

    fragColor = vec4(lighting, 1.0);
}
"""

# 全局变量
shaderProgram = None
VAO = None
texture = None
normal_texture = None

NumIndices = 0

time_count = 0

def sphere_mesh(stacks=50, slices=50):
    """生成球体的顶点、纹理坐标和法线。"""
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
            vertices.append([x, y, z, 1.0])
            texcoords.append([float(j) / slices, float(i) / stacks])
            normals.append([x, y, z])

    for i in range(stacks):
        for j in range(slices):
            p1 = i * (slices + 1) + j
            p2 = p1 + slices + 1
            indices.extend([p1, p2, p1 + 1, p2, p2 + 1, p1 + 1])

    return (
        np.array(vertices, dtype=np.float32),
        np.array(texcoords, dtype=np.float32),
        np.array(normals, dtype=np.float32),
        np.array(indices, dtype=np.uint32),
    )


def initialize():
    """初始化 OpenGL 相关设置。"""
    global shaderProgram, VAO, texture, NumIndices, normal_texture

    # 编译着色器
    vertex_shader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragment_shader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    shaderProgram = shaders.compileProgram(vertex_shader, fragment_shader)

    # 创建球体网格
    vertices, texcoords, normals, indices = sphere_mesh()
    NumIndices = len(indices)

    # 创建 VAO
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # 创建 VBO
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(
        GL_ARRAY_BUFFER,
        vertices.nbytes + texcoords.nbytes + normals.nbytes,
        None,
        GL_STATIC_DRAW,
    )
    glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)
    glBufferSubData(GL_ARRAY_BUFFER, vertices.nbytes, texcoords.nbytes, texcoords)
    glBufferSubData(
        GL_ARRAY_BUFFER, vertices.nbytes + texcoords.nbytes, normals.nbytes, normals
    )

    # 创建 EBO
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # 配置顶点属性
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(vertices.nbytes))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(
        2, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(vertices.nbytes + texcoords.nbytes)
    )
    glEnableVertexAttribArray(2)

    # 加载纹理，添加抗锯齿过滤
    texture = glGenTextures(1)
    img = np.array(Image.open("earthmap.jpg"))
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB, img.shape[1], img.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, img
    )
    glGenerateMipmap(GL_TEXTURE_2D)

    # 设置纹理过滤方式为多级纹理抗锯齿
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # 加载法线贴图
    normal_texture = glGenTextures(1)
    bump_map = np.array(Image.open("Earth-Bump-Map.jpg").convert("RGB"))    
    glBindTexture(GL_TEXTURE_2D, normal_texture)
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB, bump_map.shape[1], bump_map.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, bump_map
    )
    glGenerateMipmap(GL_TEXTURE_2D)

    # 设置法线贴图过滤方式
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)



def render():
    """渲染场景。"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glUseProgram(shaderProgram)

    # 设置 MVP 矩阵
    proj = glm.perspective(glm.radians(45.0), 640 / 480, 0.1, 100.0)
    view = glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    model = glm.mat4(1.0)
    model = glm.rotate(model, glm.radians(time_count * 5), glm.vec3(1, 1, 0))
    mvp = proj * view * model
    normal_matrix = glm.transpose(glm.inverse(glm.mat3(model)))

    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "MVP"), 1, GL_FALSE, glm.value_ptr(mvp))
    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "Model"), 1, GL_FALSE, glm.value_ptr(model))
    glUniformMatrix3fv(glGetUniformLocation(shaderProgram, "NormalMatrix"), 1, GL_FALSE, glm.value_ptr(normal_matrix))

    # 设置光源
    glUniform3f(glGetUniformLocation(shaderProgram, "LightPos"), 5.0, 5.0, 5.0)
    glUniform3f(glGetUniformLocation(shaderProgram, "LightColor"), 1.0, 1.0, 1.0)

    # 绑定纹理
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture)
    glUniform1i(glGetUniformLocation(shaderProgram, "texture0"), 0)

    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D, normal_texture)
    glUniform1i(glGetUniformLocation(shaderProgram, "normalMap"), 1)
    # 绘制球体
    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, NumIndices, GL_UNSIGNED_INT, None)
    glutSwapBuffers()

def animate(value):
    global time_count

    glutPostRedisplay()

    glutTimerFunc(200, animate, 0)
    
    time_count = time_count+1.0


def main():
    """程序入口。"""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutCreateWindow(b"Earth Texture with Anti-Aliasing")
    initialize()
    glutDisplayFunc(render)
    glutTimerFunc(200, animate, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()
