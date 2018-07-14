# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 20:57:31 2018

@author: Administrator
"""

import numpy as np
from matplotlib import pyplot as plt

M = 1000  # 小车质量：1000 kg
v = 0 # 小车初始速度
t_L = []
F_L = []
f_L = []
v_L = []
a_L = []
for i in range(0, 10000):
    F = np.abs(200 * np.sin(i/500)) + 600  # 拉力 100 N
    f = 1000 * v**2 # 摩擦阻力
    a = (F-f)/M
    v += a/1000
    t_L.append(i/1000)
    F_L.append(F)
    f_L.append(f)
    a_L.append(a)
    v_L.append(v)
    
plt.plot(t_L, F_L)
plt.show()
plt.plot(t_L, f_L)
plt.show()
plt.plot(t_L, v_L)
plt.show()












