import numpy as np
import matplotlib.pyplot as plt

# de Casteljau算法
def de_casteljau(control_points, t):
    n = len(control_points)
    points = np.array(control_points)
    while len(points) > 1:
        points = (1 - t) * points[:-1] + t * points[1:]
    return points[0]

# 生成Bezier曲线
def bezier_curve(control_points, num_points):
    curve_points = []
    for t in np.linspace(0, 1, num_points):
        curve_points.append(de_casteljau(control_points, t))
    return np.array(curve_points)

# 绘制四分之一圆弧的Bezier曲线
def draw(control_points, num_points=100):
    circle_points = bezier_curve(control_points, num_points)
    plt.plot(circle_points[:, 0], circle_points[:, 1], label='Bezier Circle')

# 绘制控制点
def draw_control(control_points):
    control_points = np.array(control_points)
    plt.plot(control_points[:, 0], control_points[:, 1],'-co',linestyle='None', label='Control Points')

def main():
    
    plt.figure(figsize=(6, 6))
    
    control_points = [[1,0],[1,0.5],[0.5,1],[0,1]]
    draw(control_points, num_points=100)
    draw_control(control_points)
    
    control_points = [[1,0],[1,-0.5],[0.5,-1],[0,-1]]
    draw(control_points, num_points=100)
    draw_control(control_points)

    control_points = [[-1,0],[-1,-0.5],[-0.5,-1],[0,-1]]
    draw(control_points, num_points=100)
    draw_control(control_points)

    control_points = [[-1,0],[-1,0.5],[-0.5,1],[0,1]]
    draw(control_points, num_points=100)
    draw_control(control_points)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.title('Bezier Curves')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.show()

# 运行主程序
if __name__ == '__main__':
    main()
