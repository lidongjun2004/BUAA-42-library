import glfw
import numpy as np
from PIL import Image
import OpenGL.GL as gl

# 渲染分辨率
WIDTH, HEIGHT = 800, 600

# 球体类
class Sphere:
    def __init__(self, center, radius, texture):
        self.center = np.array(center)
        self.radius = radius
        self.texture = np.array(Image.open(texture)) / 255.0
        self.rotation_angle = 0.0  # 初始旋转角度

    def intersect(self, ray_origin, ray_direction):
        # 与球体求交的数学公式
        oc = ray_origin - self.center
        a = np.dot(ray_direction, ray_direction)
        b = 2.0 * np.dot(oc, ray_direction)
        c = np.dot(oc, oc) - self.radius ** 2
        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return False, None
        t1 = (-b - np.sqrt(discriminant)) / (2 * a)
        t2 = (-b + np.sqrt(discriminant)) / (2 * a)
        t = min(t1, t2)
        if t > 0:
            hit_point = ray_origin + t * ray_direction
            normal = (hit_point - self.center) / self.radius
            return True, (hit_point, normal)
        return False, None

    def get_texture_color(self, hit_point):
        # 纹理坐标映射，加入旋转逻辑
        local_point = hit_point - self.center

        # 将点旋转到新的位置
        rotated_point = self.rotate_point(local_point)

        u = 0.5 + np.arctan2(rotated_point[2], rotated_point[0]) / (2 * np.pi)
        v = 0.5 - np.arcsin(rotated_point[1] / self.radius) / np.pi
        h, w, _ = self.texture.shape
        x = int(u * w) % w
        y = int(v * h) % h
        return self.texture[y, x]

    def rotate_point(self, point):
        # 绕Y轴旋转
        angle = self.rotation_angle
        rotation_matrix = np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ])
        return np.dot(rotation_matrix, point)

    def get_texture_color(self, hit_point):
        # 纹理坐标映射
        local_point = hit_point - self.center
        u = 0.5 + np.arctan2(local_point[2], local_point[0]) / (2 * np.pi)
        v = 0.5 - np.arcsin(local_point[1] / self.radius) / np.pi
        h, w, _ = self.texture.shape
        x = int(u * w) % w
        y = int(v * h) % h
        return self.texture[y, x]

# 渲染场景
def render_scene(sphere, light, camera, width, height, fov):
    image = np.zeros((height, width, 3))
    aspect_ratio = width / height
    camera_origin = np.array(camera["position"])

    for y in range(height):
        for x in range(width):
            i = (2 * (x + 0.5) / width - 1) * np.tan(fov / 2 * np.pi / 180) * aspect_ratio
            j = (1 - 2 * (y + 0.5) / height) * np.tan(fov / 2 * np.pi / 180)
            ray_direction = np.array([i, j, 1])
            ray_direction /= np.linalg.norm(ray_direction)
            color = raytrace(sphere, light, camera_origin, ray_direction)
            image[y, x] = color
    return image

# 光线追踪逻辑
def raytrace(sphere, light, ray_origin, ray_direction):
    intersect, data = sphere.intersect(ray_origin, ray_direction)
    if not intersect:
        return np.array([0.0, 0.0, 0.0])  # 背景色
    hit_point, normal = data
    light_dir = (light["position"] - hit_point)
    light_dir /= np.linalg.norm(light_dir)

    # 光照计算
    diffuse_intensity = max(np.dot(normal, light_dir), 0)
    texture_color = sphere.get_texture_color(hit_point)
    color = diffuse_intensity * texture_color * light["intensity"]
    return np.clip(color, 0, 1)

# 显示逻辑
def main():
    if not glfw.init():
        return

    window = glfw.create_window(WIDTH, HEIGHT, "Ray Tracing", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    sphere = Sphere(center=[0, 0, 3], radius=1, texture="Pic/Earth.jpg")
    light = {"position": np.array([5, 5, -2]), "intensity": np.array([1, 1, 1])}
    camera = {"position": [0, 0, -1]}

    start_time = glfw.get_time()  # 记录开始时间

    while not glfw.window_should_close(window):
        glfw.poll_events()

        # 计算时间差，更新旋转角度
        current_time = glfw.get_time()
        elapsed_time = current_time - start_time
        sphere.rotation_angle = elapsed_time  # 线性更新角度

        # 渲染场景
        image = render_scene(sphere, light, camera, WIDTH, HEIGHT, fov=90)

        # 显示图像
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glDrawPixels(WIDTH, HEIGHT, gl.GL_RGB, gl.GL_FLOAT, image)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()