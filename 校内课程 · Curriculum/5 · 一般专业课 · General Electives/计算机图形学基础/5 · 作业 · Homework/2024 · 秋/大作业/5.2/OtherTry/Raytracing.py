import numpy as np
from PIL import Image

# 定义一个类表示光线
class Ray:
    def __init__(self, origin, direction):
        self.origin = np.array(origin)
        self.direction = np.array(direction) / np.linalg.norm(direction)

# 定义一个类表示球体
class Sphere:
    def __init__(self, center, radius, color):
        self.center = np.array(center)
        self.radius = radius
        self.color = np.array(color)

    # 判断光线是否与球体相交
    def intersect(self, ray):
        oc = ray.origin - self.center
        a = np.dot(ray.direction, ray.direction)
        b = 2.0 * np.dot(oc, ray.direction)
        c = np.dot(oc, oc) - self.radius ** 2
        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return False, None
        else:
            t1 = (-b - np.sqrt(discriminant)) / (2 * a)
            t2 = (-b + np.sqrt(discriminant)) / (2 * a)
            t = min(t1, t2)
            if t > 0:
                hit_point = ray.origin + t * ray.direction
                normal = (hit_point - self.center) / self.radius
                return True, (hit_point, normal)
        return False, None

# 定义光源
class Light:
    def __init__(self, position, intensity):
        self.position = np.array(position)
        self.intensity = np.array(intensity)

# 光线追踪函数
def raytrace(ray, sphere, light):
    intersect, data = sphere.intersect(ray)
    if not intersect:
        return np.array([0, 0, 0])  # 返回背景色（黑色）
    
    hit_point, normal = data
    light_dir = (light.position - hit_point)
    light_dir /= np.linalg.norm(light_dir)

    # 简单的光照模型 (Lambertian shading)
    diffuse_intensity = max(np.dot(normal, light_dir), 0)
    color = diffuse_intensity * sphere.color * light.intensity

    return np.clip(color, 0, 1)

# 场景设置
width, height = 800, 600
aspect_ratio = width / height
fov = 90
camera_origin = np.array([0, 0, -1])  # 相机位置
image = np.zeros((height, width, 3))  # 创建图片

# 创建球体和光源
sphere = Sphere(center=[0, 0, 3], radius=1, color=[1, 0, 0])  # 红色球体
light = Light(position=[5, 5, -2], intensity=[1, 1, 1])  # 白色光源

# 遍历像素
for y in range(height):
    for x in range(width):
        # 将屏幕坐标映射到世界坐标
        i = (2 * (x + 0.5) / width - 1) * np.tan(fov / 2 * np.pi / 180) * aspect_ratio
        j = (1 - 2 * (y + 0.5) / height) * np.tan(fov / 2 * np.pi / 180)
        direction = np.array([i, j, 1])  # 光线方向（投影到 z=1 平面）
        ray = Ray(camera_origin, direction)
        
        # 获取像素颜色
        color = raytrace(ray, sphere, light)
        image[y, x] = color

# 保存图片
image = (image * 255).astype(np.uint8)  # 转换为 8 位整数
img = Image.fromarray(image)
img.save('raytraced_scene.png')