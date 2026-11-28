import numpy as np
import copy
import math
from PIL import Image

def LookAt(eye, center, up): #构建视图矩阵，将世界坐标系转化为相机坐标系

    forward = (center - eye)
    forward = forward / np.linalg.norm(forward)
    right = np.cross(forward, up)
    right = right / np.linalg.norm(right)
    up = np.cross(right, forward)
    rotation = np.eye(4)
    rotation[0, :3] = right
    rotation[1, :3] = up
    rotation[2, :3] = -forward
    translation = np.eye(4)
    translation[:3, 3] = -eye 
    view_matrix = rotation @ translation
    return view_matrix
def Ortho(left, right, bottom, top, near, far): #正交投影
    return np.eye(4)
    
def Perspective(fov, aspect=1.0, near=0.1, far=10.0): #透视投影
    mat = np.eye(4)
    mat[3, 2] = -1
    mat[3, 3] = 0
    return mat

class Triangle(object): 
    
    def __init__(self):
        
        self.vertices = np.zeros((3, 3))
        self.normals = np.eye(3)
        self.colors = np.zeros((3,3))
        self.tex_coords = np.zeros((3, 2))
    
    def setVertex(self, ind, x, y, z):
        self.vertices[ind][0] = x
        self.vertices[ind][1] = y
        self.vertices[ind][2] = z
    
    def setColor(self, ind, r, g, b):
        self.colors[ind][0] = r
        self.colors[ind][1] = g
        self.colors[ind][2] = b
    
    def setNormal(self, ind, nx, ny, nz):
        self.normals[ind][0] = x
        self.normals[ind][1] = y
        self.normals[ind][2] = z
    
    def setTexCoord(self, ind, tx, ty):
        self.tex_coords[ind][0] = tx
        self.tex_coords[ind][1] = ty

    def rotate_norm(self, thea):
        
        
        A = self.vertices[0]
        B = self.vertices[1]
        C = self.vertices[2]

        center = (A + B + C) / 3.0


    
    def rotate_mat(self, mat): #mat 3x3
        self.vertices = (mat @ self.vertices.T).T
        
        
    
    def inside(self, x, y, z): #判断点(x,y,z)是否在三角形里
        return False
        
    def to_homogeneous_coordinates(self):
        return np.hstack((self.vertices, np.ones((3, 1))))

class Rasterization(object):

    def __init__(self, width, height):

        self.color_buf = np.zeros((height, width, 3))

        self.view_m = np.eye(4) #视图矩阵
        self.proj_m = np.eye(4) #投影矩阵

    def setViewM(self, mat):
        self.view_m = mat

    def setProjM(self, mat):
        self.proj_m = mat
    
    def rasterize_triangle(self, t): #光栅化一个三角形

        H, W, _ = self.color_buf.shape

        v4 = t.to_homogeneous_coordinates()
        v4 = (self.proj_m @ self.view_m @ v4.T).T
        v4 = v4 / np.repeat(v4[:,3:], 4, axis=1)

        v4 = v4 * 0.5 + 0.5

        raster_t = Triangle()
        raster_t.setVertex(0, v4[0][0]*W, v4[0][1]*H, 0)
        raster_t.setVertex(1, v4[1][0]*W, v4[1][1]*H, 0)
        raster_t.setVertex(2, v4[2][0]*W, v4[2][1]*H, 0)
        
        for x in range(W):
            for y in range(H):
                if raster_t.inside(x, H-1-y, 0):
                    self.color_buf[y][x] = t.colors[0]
        
    
    def render(self, t_list): #渲染，输入一个三角形的list

        for t in t_list:
            self.rasterize_triangle(t)



R = Rasterization(256, 256)
R.setViewM(LookAt(np.array([0, 0, 3]), np.array([0, 0, 0]), np.array([0, 1, 0])))
R.setProjM(Perspective(60))

t = Triangle()
t.setVertex(0, 0, 1.0, 0.0)
t.setVertex(1, -1.0, 0.0, 1.0)
t.setVertex(2, 1.0, 0.0, 1.0)

t.setColor(0, 1.0, 0.0, 0.0)
t.setColor(1, 0.0, 1.0, 0.0)
t.setColor(2, 0.0, 0.0, 1.0)

R.render([t])
Image.fromarray((R.color_buf*255).astype("uint8")).show()#.save('triangle.jpg')








