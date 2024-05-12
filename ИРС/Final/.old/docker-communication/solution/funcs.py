import math
import numpy as np
import cv2
from functools import lru_cache

@lru_cache(None)
def getDistanceBetweenPoints(point1, point2):
    return math.hypot(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))


def minDistanceBetweenLines(line1, line2):
    return min([getDistanceBetweenPoints(point1, point2) for point1 in line1 for point2 in line2])


def rotateMatrix(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    rotated_matrix = [[0] * num_rows for _ in range(num_cols)]
    for i in range(num_rows):
        for j in range(num_cols):
            rotated_matrix[j][num_rows - 1 - i] = matrix[i][j]
    return rotated_matrix


def angleBetweenPoints(point1, point2):
    return math.atan2(point2[1] - point1[1], point2[0] - point1[0])

def getPointOnSameLineOnSquare(vertexes, minDist, maxDist):
    limitDist = minDist + (minDist + maxDist) // 2
    for i, pos1 in enumerate(vertexes[:-1]):
        for j, pos2 in enumerate(vertexes[i + 1:]):
            if math.hypot(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1])) < limitDist:
                return pos1, pos2

def getNearestPoints(points):
    distances = []
    for i, pnt1 in enumerate(points):
        for j, pnt2 in enumerate(points[i+1:], start=i+1):
            distances.append((getDistanceBetweenPoints(pnt1, pnt2), pnt1, pnt2))
    nearestPoints = sorted(distances, key=lambda x: x[0])[0][1:]
    return nearestPoints

def getAngleBetweenLines(line1, line2):
    startPosLine1, endPosLine1 = line1
    startPosLine2, endPosLine2 = line2
    vector1 = [(endPosLine1[axis] - startPosLine1[axis]) for axis in range(2)]
    vector2 = [(endPosLine2[axis] - startPosLine2[axis]) for axis in range(2)]
    scalarProduct = np.dot(vector1, vector2)
    lengthVector1 = math.hypot(abs(vector1[0]), abs(vector1[1]))
    lengthVector2 = math.hypot(abs(vector2[0]), abs(vector2[1]))
    lengthsProduct = lengthVector1 * lengthVector2
    if lengthsProduct == 0: return math.pi
    angle = math.acos(scalarProduct / lengthsProduct)
    return angle

def angleToPoint(centralPoint, angle, d=1):
    angle = math.radians(360 - (math.degrees(angle) + 90))
    x, y = centralPoint
    nx = x + d * math.cos(angle)
    ny = y + d * math.sin(angle)
    return nx, ny

def orderPoints(points):
    rect = np.zeros((4, 2), dtype='float32')
    s = points.sum(axis=1)
    rect[0] = points[np.argmin(s)]
    rect[2] = points[np.argmax(s)]
    diff = np.diff(points, axis=1)
    rect[1] = points[np.argmin(diff)]
    rect[3] = points[np.argmax(diff)]
    return rect


def fourPointTransform(image, corners):
    rect = orderPoints(corners)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype='float32')
    M = cv2.getPerspectiveTransform(rect, dst)
    imgWraped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return imgWraped