import numpy as np


v1 = np.concatenate((np.arange(0, 5.5, 0.2), np.arange(5.2, -0.1, -0.2), np.arange(-0.2, -5.5, -0.2), np.arange(-5.2, 0.1, 0.2)))
v2 = np.concatenate((np.arange(0, 5.1, 0.2), np.arange(4.8, -0.1, -0.2), np.arange(-0.2, -5.1, -0.2), np.arange(-4.8, 0.1, 0.2)))
img1_numbers = np.array([f"{1238 + i}" for i in range(len(v1))])
img_numbers2 = np.array([f"{1349 + i}" for i in range(len(v2))])