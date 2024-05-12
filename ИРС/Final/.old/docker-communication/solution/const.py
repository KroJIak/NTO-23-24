import numpy as np
import os

class Camera:
    def __init__(self, matrix, distortion):
        self.matrix = np.array(matrix)
        self.distortion = np.array(distortion)

class Path:
    def __init__(self):
        self.images = os.path.join('solution', 'images')

class ConstPlenty:
    def __init__(self):
        self.cam = Camera(matrix=[[1.38799238e+03, 0.00000000e+00, 9.36627601e+02],
                                  [0.00000000e+00, 1.38545890e+03, 5.76339774e+02],
                                  [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]],
                          distortion=[[0.19483555, -0.42715793, -0.00151499,  0.00274679, 0.01616779]])
        self.path = Path()