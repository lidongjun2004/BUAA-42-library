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
uniform mat4 M; // 法线变换矩阵
uniform vec3 lightPos; // 光源在世界坐标下的位置
uniform vec3 lightColor; // 光源的颜色

out vec2 vt_texcoord;
out vec3 ambient;
out vec3 diffuse;

void main() {
    gl_Position = MVP * position;

    // 环境光
    float ambientStrength = 0.02;
    ambient = ambientStrength * lightColor;

    // 漫反射
    vec3 norm = normalize(mat3(M) * norm);
    vec3 dd = lightPos - (M * position).xyz;
    vec3 lightdir = normalize(dd);
    float r2 = dot(dd, dd);
    diffuse = lightColor / r2 * max(dot(norm, lightdir), 0.0);

    vt_texcoord = texcoord;
}
"""

# 片元着色器
FRAGMENT_SHADER = """
#version 430
uniform sampler2D tex0;

in vec3 ambient;
in vec3 diffuse;
in vec2 vt_texcoord;

out vec4 fragColor;

void main() {
    vec3 kd = texture(tex0, vt_texcoord).rgb;
    vec3 color = ambient + kd * diffuse; 
    fragColor = vec4(color, 1.0);
}
"""

shaderProgram = None
VAO = None
Num_T = 0
time_count = 0


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


def initialize():
    global shaderProgram, VAO, Num_T

    vertexshader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragmentshader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

    shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)

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

    tex = glGenTextures(1)
    img = np.array(Image.open('earthmap.jpg').convert("RGB"))
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.shape[1], img.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, img)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glGenerateMipmap(GL_TEXTURE_2D)


def calc_mvp(width, height):
    proj = glm.perspective(glm.radians(60.0), float(width) / float(height), 0.1, 20.0)
    view = glm.lookAt(glm.vec3(0.0, 0.0, 3.0), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    model = glm.rotate(glm.mat4(1.0), glm.radians(time_count * 5), glm.vec3(1, 1, 0))
    return model, proj * view * model


def render():
    global shaderProgram, VAO, Num_T

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glEnable(GL_DEPTH_TEST)

    glUseProgram(shaderProgram)

    mvp_loc = glGetUniformLocation(shaderProgram, "MVP")
    m_loc = glGetUniformLocation(shaderProgram, "M")
    m_mat, mvp_mat = calc_mvp(640, 480)

    glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, glm.value_ptr(mvp_mat))
    glUniformMatrix4fv(m_loc, 1, GL_FALSE, glm.value_ptr(m_mat))

    lightPos = np.array([0.0, 0.0, 3.0], np.float32)
    lightColor = np.array([10.0, 10.0, 10.0], np.float32)
    glUniform3f(glGetUniformLocation(shaderProgram, "lightPos"), *lightPos)
    glUniform3f(glGetUniformLocation(shaderProgram, "lightColor"), *lightColor)

    glActiveTexture(GL_TEXTURE0)
    glUniform1i(glGetUniformLocation(shaderProgram, "tex0"), 0)

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
    glutCreateWindow(b"Earth Sphere with Texture")
    initialize()
    glutDisplayFunc(render)
    glutTimerFunc(200, animate, 0)
    glutMainLoop()


if __name__ == '__main__':
    main()
