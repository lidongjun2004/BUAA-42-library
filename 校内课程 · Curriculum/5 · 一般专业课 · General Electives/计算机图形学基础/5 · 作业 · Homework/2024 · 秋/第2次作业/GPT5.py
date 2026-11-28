import os
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

out vec2 fragTexcoord;
out vec3 fragPosition;
out vec3 fragNormal;

void main() {
    gl_Position = MVP * position;
    fragTexcoord = texcoord;
    fragPosition = vec3(Model * position);
    fragNormal = normalize(NormalMatrix * norm);
}
"""

# 片元着色器
# 片元着色器 - 调试法线贴图效果
FRAGMENT_SHADER = """
#version 430
in vec2 fragTexcoord;
in vec3 fragPosition;
in vec3 fragNormal;

uniform sampler2D texture0;  // 纹理贴图
uniform sampler2D normalMap; // 法线贴图
uniform vec3 LightPos;       // 光源位置
uniform vec3 LightColor;     // 光源颜色

out vec4 fragColor;

void main() {
    // 采样法线贴图
    vec3 normal = texture(normalMap, fragTexcoord).rgb;
    normal = normalize(normal * 2.0 - 1.0); // 将法线范围从 [0, 1] 转为 [-1, 1]

    // 测试阶段：输出法线颜色到屏幕
    fragColor = vec4(normal * 0.5 + 0.5, 1.0); // 映射 [-1, 1] 到 [0, 1]
    return;

    // 光照计算
    vec3 lightDir = normalize(LightPos - fragPosition);
    vec3 viewDir = normalize(-fragPosition);

    // 环境光
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * LightColor;

    // 漫反射
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = diff * LightColor;

    // 镜面反射 (Blinn-Phong)
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), 32.0);
    vec3 specular = spec * LightColor;

    // 纹理采样与光照结合
    vec3 texColor = texture(texture0, fragTexcoord).rgb;
    vec3 lighting = ambient + diffuse * texColor + specular;

    fragColor = vec4(lighting, 1.0);
}
"""

# 全局变量
shaderProgram = None
VAO = None
NumIndices = 0
texture = None
normal_map = None

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


def load_texture(file_path):
    """加载纹理图片，并确保格式正确。"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件 {file_path} 不存在，请检查路径。")

    img = Image.open(file_path).convert("RGB")  # 确保为 RGB 格式
    img_data = np.ascontiguousarray(np.array(img, dtype=np.uint8))  # 确保数据连续

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data
    )
    glGenerateMipmap(GL_TEXTURE_2D)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    return tex_id


def initialize():
    """初始化 OpenGL 相关设置。"""
    global shaderProgram, VAO, NumIndices, texture, normal_map

    # 加载纹理文件路径
    texture_file = "earthmap.jpg"
    normal_map_file = "Earth-Bump-Map.jpg"

    # 编译着色器
    vertex_shader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragment_shader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    shaderProgram = shaders.compileProgram(vertex_shader, fragment_shader)

    # 加载纹理和法线贴图
    texture = load_texture(texture_file)

    try:
        normal_map = load_texture(normal_map_file)
    except FileNotFoundError as e:
        print(f"法线贴图加载失败: {e}")
        normal_map = None  # 如果法线贴图加载失败，可设置为空以继续执行

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


def render():
    """渲染场景。"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glUseProgram(shaderProgram)

    # 设置 MVP 矩阵
    proj = glm.perspective(glm.radians(45.0), 640 / 480, 0.1, 100.0)
    view = glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    model = glm.mat4(1.0)
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

    # 如果法线贴图存在，则绑定
    if normal_map:
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, normal_map)
        glUniform1i(glGetUniformLocation(shaderProgram, "normalMap"), 1)

    # 绘制球体
    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, NumIndices, GL_UNSIGNED_INT, None)
    glutSwapBuffers()


def main():
    """程序入口。"""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutCreateWindow(b"Earth Texture with Bump Mapping")
    initialize()
    glutDisplayFunc(render)
    glutMainLoop()


if __name__ == "__main__":
    main()
