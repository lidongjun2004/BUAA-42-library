import pygame

# 初始化 Pygame
pygame.init()

# 创建窗口
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hello Pygame")

# 定义颜色
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 关闭窗口事件
            running = False
    
    # 绘制背景
    screen.fill(WHITE)
    
    # 绘制一个蓝色矩形
    pygame.draw.rect(screen, BLUE, (100, 100, 200, 100))
    
    # 更新显示
    pygame.display.flip()

# 退出 Pygame
pygame.quit()