import numpy as np
from PIL import Image
from OpenGL.GL import *
import glfw
import glm 
from AuxFunc import *

time_count = 0

# 画面长宽
width=800
height=600

# 生成球的粒度
SphereSlice=40
NumVertex=(SphereSlice+1)*(SphereSlice+1)
NumIndex=6*SphereSlice*SphereSlice

# 相机参数
eye=np.array([10, 0, 0], np.float32)
center=np.array([0, 0, 0], np.float32)
up=np.array([0, 0, 1], np.float32)

# 光线参数
lightPos = np.array([10, 0.0, 0.0], np.float32)      #设置光源位置
lightColor = np.array([50.0, 50.0, 50.0], np.float32) #设置光源亮度

# 设置帧率
TARGET_FPS = 10
frame_interval = 1.0 / TARGET_FPS


    
class Planet: # 行星
    def __init__(self, name:str, radius:float, tex_src:str, shaderProgram, position):

        self.name=name
        self.radius=radius
        self.position=np.array(position, np.float32)

        # 生成球的粒度
        SphereSlice=40
        NumVertex=(SphereSlice+1)*(SphereSlice+1)
        NumIndex=6*SphereSlice*SphereSlice

        # 生成并计算顶点索引列表, 坐标列表,纹理坐标列表和法向量列表
        indexList=np.zeros((NumIndex, ), np.uint32)
        pointList=np.zeros((NumVertex, 4), np.float32)
        texList=np.zeros((NumVertex, 2), np.float32)
        normList=np.zeros((NumVertex, 3), np.float32)

        x, y, z, u, v=0.0, 0.0, 0.0, 0.0, 0.0
        for i in range(SphereSlice+1):
            for j in range(SphereSlice+1):
                x=np.sin(self.radius*np.radians(180*i/SphereSlice))*np.cos(np.radians(360*j/SphereSlice))
                y=np.sin(self.radius*np.radians(180*i/SphereSlice))*np.sin(np.radians(360*j/SphereSlice))
                z=-np.cos(self.radius*np.radians(180*i/SphereSlice))
                u=self.radius*j/SphereSlice  # 经度映射到水平纹理坐标
                v=self.radius*(1.0-1.0*i/SphereSlice)  # 纬度映射到垂直纹理坐标
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

        Points, Norms, Texs=[], [], []
        for i in range(NumIndex):
            Points.append(pointList[indexList[i]])
            Texs.append(texList[indexList[i]])
            Norms.append(normList[indexList[i]])
    
        Points=np.array(Points, np.float32)
        Texs=np.array(Texs, np.float32)
        Norms=np.array(Norms, np.float32)
        
        # 生成并设置 VAO 和 VBO 信息（只做一次）
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # 绑定顶点坐标
        VBO1= glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO1)
        glBufferData(GL_ARRAY_BUFFER, Points.nbytes, Points, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4*4, None)
        glEnableVertexAttribArray(0)

        # 绑定纹理坐标
        VBO2=glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO2)
        glBufferData(GL_ARRAY_BUFFER, Texs.nbytes, Texs, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4*2, None)
        glEnableVertexAttribArray(1)

        # 绑定法向量
        VBO3=glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO3)
        glBufferData(GL_ARRAY_BUFFER, Norms.nbytes, Norms, GL_STATIC_DRAW)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 4*3, None)
        glEnableVertexAttribArray(2)

        # 解绑 VAO，准备渲染时使用
        glBindVertexArray(0)

        # 加载并绑定纹理
        self.texture = self.load_texture(tex_src, shaderProgram)

    def load_texture(self, tex_src, shaderProgram):
        tex = glGenTextures(1)
        img = np.array(Image.open(tex_src))
        
        if img.size == 0:
            print("Failed to load image!")
            return None
        
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.shape[1], img.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, img)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glGenerateMipmap(GL_TEXTURE_2D)

        glUniform1i(glGetUniformLocation(shaderProgram, "tex0"), 0)
        return tex

       
    def Draw(self, shaderProgram):
        
        glBindVertexArray(self.vao)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glDrawArrays(GL_TRIANGLES, 0, NumIndex) 
        calc_and_update_mvp(width, height, shaderProgram, self.position)
        glBindVertexArray(0)

def calc_and_update_mvp(width, height, shaderProgram, position):
    global time_count
    time_count=glfw.get_time()* 50
    
    proj = glm.perspective(glm.radians(60.0),float(width)/float(height),0.1,20.0)
    view = glm.lookAt(glm.vec3(eye), glm.vec3(center),glm.vec3(up))
    model =  glm.mat4(1.0)

    model = glm.rotate(model, glm.radians(time_count * 0.5), glm.vec3(0, 0, 1))

    # 添加平移
    model = glm.translate(model, glm.vec3(np.array(position, np.float32)))

    mvp = proj * view * model

    mvp_loc = glGetUniformLocation(shaderProgram,"MVP")
    m_loc = glGetUniformLocation(shaderProgram, "M")

    glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, glm.value_ptr(mvp))
    glUniformMatrix4fv(m_loc, 1, GL_FALSE, glm.value_ptr(model))

