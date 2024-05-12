import numpy as np

def distanceBetweenPositions(pos1, pos2) -> float:
    dist = ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**0.5
    return dist

def getNormalByPoints(points, radius=1):
    centerNormal = [points[len(points) // 2]] if len(points) % 2 != 0 else points[len(points) // 2 - 1:len(points) // 2 + 1]
    normalX = sum(nml.x for nml in centerNormal) / len(centerNormal)
    normalY = sum(nml.y for nml in centerNormal) / len(centerNormal)
    normal = np.array([-(normalX / radius), -(normalY / radius)])
    return normal