# -*- coding: utf-8 -*-
import time
import matplotlib.pyplot as plt
plt.plot([1,2,3,4])
plt.ylabel('some numbers')
plt.show()


import numpy as np
import matplotlib.pyplot as plt

# 0到5之间每隔0.2取一个数
t = np.arange(0., 5., 0.2)

# 红色的破折号，蓝色的方块，绿色的三角形
plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
plt.show()

time.sleep(999999)