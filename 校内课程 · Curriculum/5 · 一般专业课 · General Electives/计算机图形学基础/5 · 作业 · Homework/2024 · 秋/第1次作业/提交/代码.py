import numpy as np
import math
from PIL import Image

def LookAt(eye, center, up):
    forward = (center - eye)
    forward = forward / np.linalg.norm(forward)
    right = np.cross(forward, up)
    right = right / np.linalg.norm(right)
    up = np.cross(right, forward)
    rot = np.eye(4)
    rot[0, :3] = right
    rot[1, :3] = up
    rot[2, :3] = -forward
    trans = np.eye(4)
    trans[:3, 3] = -eye 
    mat = rot @ trans
    return mat

def Ortho(left, right, bottom, top, near, far):
    mat = np.eye(4)
    mat[0, 0] = 2 / (right - left)
    mat[1, 1] = 2 / (top - bottom)
    mat[2, 2] = -2 / (far - near)
    mat[0, 3] = -(right + left) / (right - left)
    mat[1, 3] = -(top + bottom) / (top - bottom)
    mat[2, 3] = -(far + near) / (far - near)
    return mat

def Perspective(fov, aspect=1.0, near=0.1, far=10.0):
    f = 1 / np.tan(np.radians(fov) / 2)
    mat = np.eye(4)
    mat[0, 0] = f / aspect
    mat[1, 1] = f
    mat[2, 2] = (far + near) / (near - far)
    mat[2, 3] = 2 * far * near / (near - far)
    mat[3, 2] = -1
    mat[3, 3] = 0
    return mat

class Triangle:
    def __init__(self):
        self.vertices = np.zeros((3, 3))
        self.colors = np.zeros((3, 3))

    def setVertex(self, ind, x, y, z):
        self.vertices[ind] = [x, y, z]
    
    def setColor(self, ind, r, g, b):
        self.colors[ind] = [r, g, b]
    
    def to_homogeneous_coordinates(self):
        return np.hstack((self.vertices, np.ones((3, 1))))
    
    def inside(self, x, y, z): 
        A, B, C = self.vertices[0], self.vertices[1], self.vertices[2]
        P = np.array([x, y, z])

        AB, AC = B - A, C - A
        normal = np.cross(AB, AC)
        normal /= np.linalg.norm(normal)
    
        if not np.isclose(np.dot(P - A, normal), 0):
            return False
    
        A_2D, B_2D, C_2D = A[:2], B[:2], C[:2]
        area_total = np.cross(B_2D - A_2D, C_2D - A_2D)
        alpha = np.cross(B_2D - P[:2], C_2D - P[:2]) / area_total
        beta = np.cross(C_2D - P[:2], A_2D - P[:2]) / area_total
        gamma = 1 - alpha - beta

        return (alpha >= 0) and (beta >= 0) and (gamma >= 0), alpha, beta, gamma

    
    def rotate_norm(self, theta):
        A, B, C = self.vertices
        center = (A + B + C) / 3
        AB, AC = B - A, C - A
        normal = np.cross(AB, AC)
        normal = normal / np.linalg.norm(normal)
        theta_rad = np.radians(theta)
        cos_theta, sin_theta = np.cos(theta_rad), np.sin(theta_rad)
        u, v, w = normal
        rot = np.array([
            [cos_theta + u*u*(1 - cos_theta), u*v*(1 - cos_theta) - w*sin_theta, u*w*(1 - cos_theta) + v*sin_theta],
            [v*u*(1 - cos_theta) + w*sin_theta, cos_theta + v*v*(1 - cos_theta), v*w*(1 - cos_theta) - u*sin_theta],
            [w*u*(1 - cos_theta) - v*sin_theta, w*v*(1 - cos_theta) + u*sin_theta, cos_theta + w*w*(1 - cos_theta)]
        ])
        for i in range(3):
            self.vertices[i] = rot @ (self.vertices[i] - center) + center
    def rotate_mat(self, mat): #mat 3x3
        self.vertices = (mat @ self.vertices.T).T

class Rasterization:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color_buf = np.zeros((height, width, 3))
        self.depth_buf = np.full((height, width), np.inf)
        self.proj_m = np.eye(4)

    def setViewM(self, mat):
        self.view_m = mat

    def setProjM(self, mat):
        self.proj_m = mat

    def rasterize_triangle(self, t, interpolate_colors):
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
                inside,alpha,beta,gamma=raster_t.inside(x, H-1-y, 0)
                if inside:
                    if interpolate_colors:
                        self.color_buf[y][x] = alpha * t.colors[0] + beta * t.colors[1] + gamma * t.colors[2]
                    else:
                        self.color_buf[y][x] = t.colors[0]

    def render(self, triangles, interpolate_colors=True):
        for t in triangles:
            self.rasterize_triangle(t, interpolate_colors)


# a1
t = Triangle()
t.setVertex(0, 0, 1, 0)
t.setVertex(1, -1, 0, 1)
t.setVertex(2, 1, 0, 1)
t.setColor(0, 1, 0, 0)
t.setColor(1, 0, 1, 0)
t.setColor(2, 0, 0, 1)
R_perspective = Rasterization(256, 256)
R_perspective.setViewM(LookAt(np.array([0, 0, 3]), np.array([0, 0, 0]), np.array([0, 1, 0])))
R_perspective.setProjM(Perspective(60))
R_perspective.render([t], interpolate_colors=False)
Image.fromarray((R_perspective.color_buf * 255).astype("uint8")).save('perspective_projection.png')


#c
t = Triangle()
t.setVertex(0, 0, 1, 0)
t.setVertex(1, -1, 0, 1)
t.setVertex(2, 1, 0, 1)
t.setColor(0, 1, 0, 0)
t.setColor(1, 0, 1, 0)
t.setColor(2, 0, 0, 1)
R_perspective.render([t], True)
Image.fromarray((R_perspective.color_buf * 255).astype("uint8")).save('c.png')


# a2
t = Triangle()
t.setVertex(0, 0, 1, 0)
t.setVertex(1, -1, 0, 1)
t.setVertex(2, 1, 0, 1)
t.setColor(0, 1, 0, 0)
t.setColor(1, 0, 1, 0)
t.setColor(2, 0, 0, 1)
R_ortho = Rasterization(256, 256)
R_ortho.setViewM(LookAt(np.array([0, 0, 3]), np.array([0, 0, 0]), np.array([0, 1, 0])))
R_ortho.setProjM(Ortho(-1, 1, -1, 1, 0.1, 10))
R_ortho.render([t], False)
Image.fromarray((R_ortho.color_buf * 255).astype("uint8")).save('orthographic_projection.png')


# b
angles = [45, 90, 135, 180]

for angle in angles:
    t = Triangle()
    t.setVertex(0, 0, 1, 0)
    t.setVertex(1, -1, 0, 1)
    t.setVertex(2, 1, 0, 1)
    t.setColor(0, 1, 0, 0)
    t.setColor(1, 0, 1, 0)
    t.setColor(2, 0, 0, 1)
    t.rotate_norm(angle)
    R_rotate = Rasterization(256, 256)
    R_rotate.setViewM(LookAt(np.array([0, 0, 3]), np.array([0, 0, 0]), np.array([0, 1, 0])))
    R_rotate.setProjM(Perspective(60))
    R_rotate.render([t], False)
    Image.fromarray((R_rotate.color_buf * 255).astype("uint8")).save(f'rotation_{angle}.png')


#d
t1 = Triangle()
t1.setVertex(0, 1, 0, 0)
t1.setVertex(1, 0, 1, 0)
t1.setVertex(2, 0, 0, 1)
t1.setColor(0, 1, 0, 0)
t1.setColor(1, 1, 0, 0)
t1.setColor(2, 1, 0, 0)
t2 = Triangle()
t2.setVertex(0, 1.5, 0, 0)
t2.setVertex(1, 0, 1.5, 0)
t2.setVertex(2, 0, 0, 1.5)
t2.setColor(0, 0, 1, 0)
t2.setColor(1, 0, 1, 0)
t2.setColor(2, 0, 1, 0)
R_depth = Rasterization(256, 256)
R_depth.setViewM(LookAt(np.array([0, 0, 3]), np.array([0, 0, 0]), np.array([0, 1, 0])))
R_depth.setProjM(Perspective(60))
R_depth.render([t2, t1], interpolate_colors=True)
Image.fromarray((R_depth.color_buf * 255).astype("uint8")).save('depth_test.png')


# e
def rotation_x(angle):
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ])

def rotation_y(angle):
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c]
    ])

def rotation_z(angle):
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])
interp_tri = Triangle()
interp_tri.setVertex(0, 0, 0, 0)
interp_tri.setVertex(1, 1, 0 ,0)
interp_tri.setVertex(2, 0, 0, 1)
for t in np.linspace(0, 1, 5):
    interp_tri.setColor(0, 1-t, t, 0)
    interp_tri.setColor(1, 1-t, t, 0)
    interp_tri.setColor(2, 1-t, t, 0)
    r=rotation_x(30)@rotation_y(60)@rotation_z(30)
    interp_tri.rotate_mat(r)
    R_interp = Rasterization(256, 256)
    R_interp.setViewM(LookAt(np.array([0, 0, 3]), np.array([0, 0, 0]), np.array([0, 1, 0])))
    R_interp.setProjM(Perspective(60))
    R_interp.render([interp_tri], True)
    Image.fromarray((R_interp.color_buf * 255).astype("uint8")).save(f'color_interpolation_{int(t*100)}.png')