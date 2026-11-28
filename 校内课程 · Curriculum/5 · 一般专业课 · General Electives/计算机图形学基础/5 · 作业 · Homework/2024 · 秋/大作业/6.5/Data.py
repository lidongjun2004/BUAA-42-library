import numpy as np

# 球体信息
PlanetDataOriginal = {'Mercury':[24.40, 579100.00, 87.9693*24, 58.65*24],
               'Venus':[60.73, 1082089.30, 224.70*24, -243*24],
               'Earth':[63.78, 1496000.00, 365*24,24],
               'Mars':[67.94, 2279400.00, 686.98*24, 24.5],
               'Jupiter':[1429.84, 7783300.00, 4332.589*24, 10],
               'Saturn':[1193.00, 14270000.00, 10759.5*24, 10.6],
               'Uranus':[518.00, 28690000.00, 84.32*365*24, 17.25],
               'Neptune':[495.32, 45000000.00, 164.8*365*24, 16.1],
               }
# 原始太阳系数据,依次为:名称,行星半径,公转半径,公转周期,自转周期(公转/自转均以自西向东为正)
# 其中金星的自转周期取负数,是因为金星自转方向自东向西.

PlanetDataOptimized = {'Mercury':[24.40, 57910000, 87.9693*24, 58.65*24],
               'Venus':[60.73, 108208930, 224.70*24, -243*24],
               'Earth':[63.78, 149600000, 365*24,24],
               'Mars':[67.94, 227940000, 686.98*24, 24.5],
               'Jupiter':[142.984*1.5, 778330000, 4332.589*24, 10],
               'Saturn':[119.300*1.5, 1427000000, 10759.5*24, 10.6],
               'Uranus':[51.800*2, 2869000000, 84.32*365*24, 17.25],
               'Neptune':[49.532*2, 4500000000, 164.8*365*24, 16.1],
               }
# 优化后的太阳系数据.部分星球的行星半径调整了比例(乘除倍数).后续还会在main.py中还通过非线性缩放进一步处理.

def GetViewSettings(radius):
    
    eye=np.array([radius, 0, 0], np.float32)
    up=np.array([0, 0, 1], np.float32)
    center=np.array([0, 0, 0], np.float32)

    # 初始相机参数

    XEye=np.array([radius, 0, 0], np.float32)
    XUp=np.array([0, 0, 1], np.float32)
    XCenter=np.array([0, 0, 0], np.float32)

    YEye=np.array([0, radius, 0], np.float32)
    YUp=np.array([0, 0, 1], np.float32)
    YCenter=np.array([0, 0, 0], np.float32)

    ZEye=np.array([0, 0, radius], np.float32)
    ZUp=np.array([1, 0, 0], np.float32)
    ZCenter=np.array([0, 0, 0], np.float32)

    OriLocation=[[XEye, XUp, XCenter], 
                [YEye, YUp, YCenter],
                [ZEye, ZUp, ZCenter]]

    return eye, center, up, OriLocation