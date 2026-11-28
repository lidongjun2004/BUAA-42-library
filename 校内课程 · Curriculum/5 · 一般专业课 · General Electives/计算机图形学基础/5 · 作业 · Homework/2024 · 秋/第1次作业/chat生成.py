import numpy as np
import math
from PIL import Image

def LookAt(eye, center, up):
    forward = (center - eye)
    forward /= np.linalg.norm(forward)
    right = np.cross(forward, up)
    right /= np.linalg.norm(right)
    up = np.cross(right, forward)
    rot = np.eye(4)
    rot[0, :3] = right
    rot[1, :3] = up
    rot[2, :3] = -forward
    trans = np.eye(4)
    trans[:3, 3] = -eye
    return rot @ trans

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
        self.colors = np.zeros((3,3))

    def setVertex(self, ind, x, y, z):
        self.vertices[ind] = [x, y, z]

    def setColor(self, ind, r, g, b):
        self.colors[ind] = [r, g, b]

    def rotate_norm(self, theta):
        A, B, C = self.vertices
        center = (A + B + C) / 3
        AB, AC = B - A, C - A
        normal = np.cross(AB, AC)
        normal /= np.linalg.norm(normal)
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

class Rasterization:
    def __init__(self, width, height):
        self.color_buf = np.zeros((height, width, 3))
        self.z_buf = np.full((height, width), np.inf)
        self.view_m = np.eye(4)
        self.proj_m = np.eye(4)

    def setViewM(self, mat):
        self.view_m = mat

    def setProjM(self, mat):
        self.proj_m = mat

    def barycentric_coords(self, x, y, A, B, C):
        area_total = np.cross(B - A, C - A)
        alpha = np.cross(B - np.array([x, y]), C - np.array([x, y])) / area_total
        beta = np.cross(C - np.array([x, y]), A - np.array([x, y])) / area_total
        gamma = 1 - alpha - beta
        return alpha, beta, gamma

    def rasterize_triangle(self, t):
        H, W, _ = self.color_buf.shape
        for x in range(W):
            for y in range(H):
                alpha, beta, gamma = self.barycentric_coords(x, y, *t.vertices)
                if alpha >= 0 and beta >= 0 and gamma >= 0:
                    z = alpha * t.vertices[0][2] + beta * t.vertices[1][2] + gamma * t.vertices[2][2]
                    if z < self.z_buf[y, x]:
                        self.z_buf[y, x] = z
                        color = alpha * t.colors[0] + beta * t.colors[1] + gamma * t.colors[2]
                        self.color_buf[y, x] = color

# Task implementations
t1 = Triangle()
t1.setVertex(0, 0, 1, 0)
t1.setVertex(1, -1, 0, 1)
t1.setVertex(2, 1, 0, 1)
t1.setColor(0, 1, 0, 0)
t1.setColor(1, 0, 1, 0)
t1.setColor(2, 0, 0, 1)

# Perspective Projection
R_perspective = Rasterization(256, 256)
R_perspective.setViewM(LookAt(np.array([0, 0, 3]), np.array([0, 0, 0]), np.array([0, 1, 0])))
R_perspective.setProjM(Perspective(60))
R_perspective.rasterize_triangle(t1)
Image.fromarray((R_perspective.color_buf * 255).astype("uint8")).save('perspective_projection.jpg')

# Orthographic Projection
R_ortho = Rasterization(256, 256)
R_ortho.setViewM(LookAt(np.array([0, 0, 3]), np.array([0, 0, 0]), np.array([0, 1, 0])))
R_ortho.setProjM(Ortho(-1, 1, -1, 1, 0.1, 10))
R_ortho.rasterize_triangle(t1)
Image.fromarray((R_ortho.color_buf * 255).astype("uint8")).save('orthographic_projection.jpg')

# Rotation at Different Angles
angles = [45, 90, 135, 180]
for angle in angles:
    t_rotated = Triangle()
    t_rotated.vertices = t1.vertices.copy()
    t_rotated.colors = t1.colors.copy()
    t_rotated.rotate_norm(angle)
    R_rotated = Rasterization(256, 256)
    R_rotated.setViewM(LookAt(np.array([0, 0, 3]), np.array([0, 0, 0]), np.array([0, 1, 0])))
    R_rotated.setProjM(Perspective(60))
    R_rotated.rasterize_triangle(t_rotated)
    Image.fromarray((R_rotated.color_buf * 255).astype("uint8")).save(f'rotated_{angle}.jpg')

# Depth Test with Two Triangles
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
R_depth.rasterize_triangle(t1)
R_depth.rasterize_triangle(t2)
Image.fromarray((R_depth.color_buf * 255).astype("uint8")).save('depth_test.jpg')

# Rotation and Color Interpolation Over Time
times = [0, 0.25, 0.5, 0.75, 1]
for t in times:
    t_interp = Triangle()
    t_interp.setVertex(0, (1 - t) * 0 + t * 1, (1 - t) * 0 + t * 1, 0)
    t_interp.setVertex(1, (1 - t) * 1 + t * 0, (1 - t) * 1 + t * 0, 0)
    t_interp.setVertex(2, (1 - t) * 0 + t * 0, (1 - t) * 1 + t * 0, 1)
    t_interp.setColor(0, 1, 0, t)
    t_interp.setColor(1, 0, t, 1 - t)
    t_interp.setColor(2, t, 1 - t, 0)
    R_time = Rasterization(256, 256)
    R_time.setViewM(LookAt(np.array([0, 0, 3]), np.array([0, 0, 0]), np.array([0, 1, 0])))
    R_time.setProjM(Perspective(60))
    R_time.rasterize_triangle(t_interp)
    Image.fromarray((R_time.color_buf * 255).astype("uint8")).save(f'rotation_interpolation_{t}.jpg')
