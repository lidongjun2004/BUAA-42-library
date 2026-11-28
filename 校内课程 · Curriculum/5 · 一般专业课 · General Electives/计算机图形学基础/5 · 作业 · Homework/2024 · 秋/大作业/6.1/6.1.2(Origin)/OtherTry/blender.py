# import sys
# sys.path.append('/Applications/Blender.app/Contents/Resources/2.93/python/lib/python3.7/site-packages')
import bpy

# 删除场景中的所有对象
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 创建一个球体
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))

# 获取球体对象
sphere = bpy.context.active_object
sphere.name = "MySphere"

# 设置球体材质
material = bpy.data.materials.new(name="SphereMaterial")
material.use_nodes = True  # 启用节点
sphere.data.materials.append(material)

# 设置材质的基础颜色（使用节点）
principled_bsdf = material.node_tree.nodes['Principled BSDF']
principled_bsdf.inputs['Base Color'].default_value = (1, 0, 0, 1)  # 红色

# 设置场景的渲染引擎为 Cycles（高质量光线追踪）
bpy.context.scene.render.engine = 'CYCLES'

# 设置摄像机
camera = bpy.data.objects['Camera']
camera.location = (5, -5, 5)
camera.rotation_euler = (1.1, 0, 0.8)  # 设置角度，使摄像机朝向球体

# 设置光源
light = bpy.data.objects['Light']
light.location = (4, -4, 4)
light.data.type = 'POINT'
light.data.energy = 1000  # 设置光源亮度

# 渲染图像
bpy.context.scene.render.filepath = "/tmp/sphere_render.png"
bpy.ops.render.render(write_still=True)

print("Rendering complete, saved to /tmp/sphere_render.png")