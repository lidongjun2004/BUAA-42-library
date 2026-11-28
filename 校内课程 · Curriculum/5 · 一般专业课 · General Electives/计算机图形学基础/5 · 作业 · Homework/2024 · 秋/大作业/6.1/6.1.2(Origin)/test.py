import glfw
# 进行glfw初始化
if not glfw.init():
    SystemError(-1)

# 设置画面大小(必须要先glfw.init())
mode = glfw.get_video_mode(glfw.get_primary_monitor()) # 获取显示器分辨率
width, height=int(mode.size.width), int(mode.size.height)
print(width, height)