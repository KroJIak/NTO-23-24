import numpy as np
import os
from copy import copy

class Camera:
    def __init__(self, matrix, distortion):
        self.matrix = np.array(matrix)
        self.distortion = np.array(distortion)

class Path:
    def __init__(self):
        self.images = os.path.join('', 'images')

class ConstPlenty:
    def __init__(self):
        self.cam1 = Camera(matrix=[[951.6447409, 0., 601.28670737],
                                   [0., 952.68412683, 464.89843992],
                                   [0., 0., 1.]],
                           distortion=[[-0.45733346, 0.2497311, -0.00263185, -0.00254355, -0.07533089]])
        self.cam2 = Camera(matrix=[[920.91593381, 0., 647.37763074],
                                   [0., 921.31953503, 401.63905933],
                                   [0., 0., 1.]],
                           distortion=[[-0.30131843, 0.11964215, 0.00164663, -0.00087653, -0.02382259]])
        self.path = Path()