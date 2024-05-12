import numpy as np

# получает нормаль точек
def getNormalByPoints(points, radius=1):
    centerNormal = [points[len(points) // 2]] if len(points) % 2 != 0 else points[len(points) // 2 - 1:len(points) // 2 + 1]
    normalX = sum(nml.x for nml in centerNormal) / len(centerNormal)
    normalY = sum(nml.y for nml in centerNormal) / len(centerNormal)
    normal = np.array([-(normalX / radius), -(normalY / radius)])
    return normal