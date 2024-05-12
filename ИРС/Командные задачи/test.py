import cv2
from functools import lru_cache
from math import hypot
from collections import deque

def showImage(img, winName='Image'):
    while cv2.waitKey(1) != 27: cv2.imshow(winName, img)

def cutMainImage(img, coefApprox=0.001, show=False):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imgBinary = cv2.threshold(imgGray, 160, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(imgBinary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    sortedContours = sorted(contours, key=cv2.contourArea)

    cnt = sortedContours[-3]
    epsilon = coefApprox * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    contourVertexes = [(pos[0][0], pos[0][1]) for pos in approx]

    if show:
        copyImg = img.copy()
        cv2.drawContours(copyImg, sortedContours, -1, (255, 255, 0), 2)
        [cv2.circle(copyImg, pos, 4, (0, 0, 255), 7) for pos in contourVertexes]
        showImage(copyImg)

    minXValue = sorted([pos[0] for pos in contourVertexes])[0]
    minYValue = sorted([pos[1] for pos in contourVertexes])[0]
    maxXValue = sorted([pos[0] for pos in contourVertexes])[-1]
    maxYValue = sorted([pos[1] for pos in contourVertexes])[-1]
    newImg = img[minYValue:maxYValue, minXValue:maxXValue]
    return (minXValue, minYValue), newImg

def getContoursObstacles(img, minArea=9000, show=False):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imgBinary = cv2.threshold(imgGray, 120, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(imgBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    sortedContours = [cnt for cnt in sorted(contours, key=cv2.contourArea) if cv2.contourArea(cnt) > minArea]
    sortedContours.pop(-1)
    if show:
        for cnt in sortedContours:
            copyImg = img.copy()
            cv2.drawContours(copyImg, [cnt], -1, (255, 255, 0), 2)
            showImage(copyImg)
    return sortedContours

def getActivePoints(img, deviation, contours, div=50, freqPoints=30, minDistPoints=60, show=False):
    points = [[(j, i) for j in range(div, img.shape[1] - div, freqPoints)]
              for i in range(div, img.shape[0] - div, freqPoints)]
    if show: copyImg = img.copy()
    for i, line in enumerate(points):
        for j, point in enumerate(line):
            for cnt in contours:
                isInside = cv2.pointPolygonTest(cnt, point, False)
                if isInside == 1: break
                distance = cv2.pointPolygonTest(cnt, point, True)
                if abs(distance) < minDistPoints: break
            else:
                if show: cv2.circle(copyImg, point, 2, (0, 0, 255), 2)
                points[i][j] = (points[i][j][0]+deviation[0], points[i][j][1]+deviation[1])
                continue
            points[i][j] = None
    if show: showImage(copyImg)
    return points

@lru_cache(maxsize=200)
def getDistanceBetweenPoints(point1, point2):
    return hypot(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))

def getNearestPoint(curPoint, dictPoints):
    nearestPoint = None
    minDist = float('inf')
    for pointId, pointPos in dictPoints.items():
        dist = getDistanceBetweenPoints(curPoint, pointPos)
        if dist < minDist:
            minDist = dist
            nearestPoint = pointId
    return nearestPoint

def getMergeListWithAruco(img, points, dictAruco, show=False):
    dictPoints = {}
    mergeList = {}
    if show: copyImg = img.copy()
    for i, line in enumerate(points):
        for j, point in enumerate(line):
            if point is None: continue
            numPoint = i*len(points[0])+j
            numRightPoint = i*len(points[0])+j+1
            numDownPoint = (i+1)*len(points[0])+j
            dictPoints[f'p_{numPoint}'] = point
            if j+1 < len(points[0]) and line[j+1] is not None:
                if show: cv2.line(copyImg, point, line[j+1], (255, 255, 0), 2)
                if f'p_{numPoint}' not in mergeList: mergeList[f'p_{numPoint}'] = [f'p_{numRightPoint}']
                else: mergeList[f'p_{numPoint}'].append(f'p_{numRightPoint}')
                if f'p_{numRightPoint}' not in mergeList: mergeList[f'p_{numRightPoint}'] = [f'p_{numPoint}']
                else: mergeList[f'p_{numRightPoint}'].append(f'p_{numPoint}')
            if i+1 < len(points) and points[i+1][j] is not None:
                if show: cv2.line(copyImg, point, points[i+1][j], (255, 255, 0), 2)
                if f'p_{numPoint}' not in mergeList: mergeList[f'p_{numPoint}'] = [f'p_{numDownPoint}']
                else: mergeList[f'p_{numPoint}'].append(f'p_{numDownPoint}')
                if f'p_{numDownPoint}' not in mergeList: mergeList[f'p_{numDownPoint}'] = [f'p_{numPoint}']
                else: mergeList[f'p_{numDownPoint}'].append(f'p_{numPoint}')
    showImage(copyImg)

    for arucoId, arucoPos in dictAruco.items():
        nearestPoint = getNearestPoint(arucoPos, dictPoints)
        mergeList[arucoId] = [nearestPoint]
        mergeList[nearestPoint].append(arucoId)

    notation = dict(list(dictAruco.items()) + list(dictPoints.items()))
    return notation, mergeList

def bfs(mergeList, start, end):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current not in visited:
            neighbors = mergeList[current]
            for neighbor in neighbors:
                if neighbor == end: return path + [neighbor]
                else: queue.append((neighbor, path + [neighbor]))
            visited.add(current)
    return []

def main():
    # s1 = NTO-docker/workspace/nto_robotics/data/ex1-map.png
    dictAruco = {'a_199': (1774, 879), 'a_19': (147, 854), 'a_94': (1111, 812), 'a_105': (1414, 813),
                 'a_79': (622, 792), 'a_175': (754, 614), 'a_26': (1578, 584), 'a_43': (270, 532), 'a_229': (1307, 458),
                 'a_99': (951, 418), 'a_255': (588, 396), 'a_213': (1628, 276), 'a_37': (964, 221), 'a_12': (230, 190),
                 'a_113': (540, 166), 'a_126': (1448, 164)}
    pointCenter = (400, 200)
    img = cv2.imread('2023-12-15_05-26.png')
    deviation, cutImg = cutMainImage(img, show=True)

    contoursObstacles = getContoursObstacles(cutImg, show=True)
    activePoints = getActivePoints(cutImg, deviation, contoursObstacles, show=True)
    notation, mergeList = getMergeListWithAruco(img, activePoints, dictAruco, show=True)

    nearestPointByRobot = getNearestPoint(pointCenter, notation)
    way = bfs(mergeList, nearestPointByRobot, list(dictAruco.keys())[0])
    copyImg = img.copy()
    for i, point in enumerate(way[:-1]):
        cv2.line(copyImg, notation[point], notation[way[i+1]], (255, 255, 0), 2)
    showImage(copyImg)


if __name__ == '__main__':
    main()