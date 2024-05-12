from math import hypot, acos, pi, degrees, ceil
from functools import lru_cache
import numpy as np
import base64
import cv2
import os


def adjustPath(file):
    import sys
    path = '/'.join(file.split('/')[:-1])
    sys.path.insert(1, path)


def readInput():
    imageString = input()
    robotPos = list(map(int, input().split()))
    countPoints = int(input())
    mainPoints = eval(input())

    buffer = base64.b64decode(imageString)
    array = np.frombuffer(buffer, dtype=np.uint8)
    img = cv2.imdecode(array, flags=1)

    return img, robotPos, countPoints, mainPoints


ALL_ARUCO_KEYS = [1, 2, 3, 5, 6, 7, 10, 11, 12, 13, 14, 15, 17, 18, 19, 21, 22, 23, 26, 27, 28, 29, 30, 31, 33, 35, 37,
                  39, 41, 42, 43, 44, 45, 46, 47, 49, 51, 53, 55, 57, 58, 59, 60, 61, 62, 63, 69, 70, 71, 76, 77, 78,
                  79, 85, 86, 87, 92, 93, 94, 95, 97, 98, 99, 101, 102, 103, 105, 106, 107, 109, 110, 111, 113, 114,
                  115, 117, 118, 119, 121, 122, 123, 125, 126, 127, 141, 142, 143, 157, 158, 159, 171, 173, 175, 187,
                  189, 191, 197, 199, 205, 206, 207, 213, 215, 221, 222, 223, 229, 231, 237, 239, 245, 247, 253, 255,
                  327, 335, 343, 351, 367, 383]


def showImage(img, winName='Image'):
    while cv2.waitKey(1) != 27: cv2.imshow(winName, img)


def rotateImage(img, rotationPoint, theta, width, height):
    shape = (img.shape[1], img.shape[0])
    matrix = cv2.getRotationMatrix2D(center=rotationPoint, angle=degrees(theta), scale=1)
    resultImg = cv2.warpAffine(src=img, M=matrix, dsize=shape)
    x = int(rotationPoint[0] - width / 2)
    y = int(rotationPoint[1] - height / 2)
    resultImg = resultImg[y:y + height, x:x + width]
    return resultImg


def getAngleBetweenLines(line1, line2):
    startPosLine1, endPosLine1 = line1
    startPosLine2, endPosLine2 = line2
    vector1 = [(endPosLine1[axis] - startPosLine1[axis]) for axis in range(2)]
    vector2 = [(endPosLine2[axis] - startPosLine2[axis]) for axis in range(2)]
    scalarProduct = np.dot(vector1, vector2)
    lengthVector1 = hypot(abs(vector1[0]), abs(vector1[1]))
    lengthVector2 = hypot(abs(vector2[0]), abs(vector2[1]))
    lengthsProduct = lengthVector1 * lengthVector2
    if lengthsProduct == 0: return pi
    angle = acos(scalarProduct / lengthsProduct)
    return angle


def getAngleBetweenLineAndAxis(line):
    startPosLine, endPosLine = line
    vector = [(endPosLine[axis] - startPosLine[axis]) for axis in range(2)]
    angles = {'x': pi, 'y': pi}
    for i, axis in enumerate(angles):
        scalarProduct = vector[i]
        lengthsProduct = hypot(vector[0], vector[1])
        if lengthsProduct == 0: continue
        resAngle = acos(scalarProduct / lengthsProduct) if axis == 'x' else acos(scalarProduct / lengthsProduct)
        if scalarProduct < 0: resAngle *= -1
        angles[axis] = resAngle
    return angles


def getPointOnSameLineOnSquare(vertexes, minDist, maxDist):
    limitDist = minDist + (minDist + maxDist) // 2
    for i, pos1 in enumerate(vertexes[:-1]):
        for j, pos2 in enumerate(vertexes[i + 1:]):
            if hypot(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1])) < limitDist:
                return pos1, pos2


def findContourCenter(cnt):
    cx, cy = None, None
    moment = cv2.moments(cnt)
    if moment['m00'] != 0:
        cx = int(moment['m10'] / moment['m00'])
        cy = int(moment['m01'] / moment['m00'])
    return (cx, cy)


def detectAruco(img, size, areaRange=[2000, 4000], coefApprox=0.03, show=False):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imgBinary = cv2.threshold(imgGray, 160, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(imgBinary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # [print(i, cv2.contourArea(cnt)) for i, cnt in enumerate(sorted(contours, key=cv2.contourArea, reverse=True))]

    arucoContours = [cnt for cnt in contours if areaRange[0] < cv2.contourArea(cnt) < areaRange[1]]
    if not arucoContours: return {}
    dictAruco = {}

    if show: imgContours = img.copy()
    for cnt in arucoContours:
        epsilon = coefApprox * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        contourVertexes = [(pos[0][0], pos[0][1]) for pos in approx]
        centerContour = (round(sum([pos[0] for pos in contourVertexes]) / 4),
                         round(sum([pos[1] for pos in contourVertexes]) / 4))
        allDistBetweenPoints = [round(hypot(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1])))
                                for i, pos1 in enumerate(contourVertexes[:-1])
                                for j, pos2 in enumerate(contourVertexes[i + 1:])]
        widthContour, heightContour = sorted(allDistBetweenPoints)[:2]
        pointContour1, pointContour2 = getPointOnSameLineOnSquare(contourVertexes,
                                                                  min(allDistBetweenPoints), max(allDistBetweenPoints))
        angleBetweenContourAndAbscissa = getAngleBetweenLines((pointContour2, pointContour1),
                                                              (pointContour1, (10, pointContour1[1])))
        imgAruco = rotateImage(img, centerContour, angleBetweenContourAndAbscissa, widthContour, heightContour)
        imgAruco = cv2.cvtColor(imgAruco, cv2.COLOR_BGR2GRAY)
        shapeImgAruco = imgAruco.shape[:2]
        sizeOneCell = (shapeImgAruco[1] / (size + 2), shapeImgAruco[0] / (size + 2))
        arucoArray = np.zeros((size, size), dtype=np.uint8)
        for i in range(size):
            for j in range(size):
                basePosX, basePosY = sizeOneCell[0] * 1.5, sizeOneCell[1] * 1.5
                posX, posY = round(basePosX + sizeOneCell[0] * j), round(basePosY + sizeOneCell[1] * i)
                valueCell = imgAruco[posY, posX]
                arucoArray[i, j] = int(bool(valueCell))
                if show: cv2.circle(imgAruco, (posX, posY), 1, (100, 100, 100), 2)
        if show: showImage(imgAruco, winName='Aruco')
        for i in range(4):
            cpArucoArray = arucoArray.copy()
            cpArucoArray.resize(size ** 2)
            numberAruco = int(''.join(list(map(str, cpArucoArray))), 2)
            if numberAruco in ALL_ARUCO_KEYS: break
            arucoArray = np.rot90(arucoArray)
        else:
            continue
        dictAruco[f'p_{numberAruco}'] = centerContour
        if show: cv2.putText(imgContours, str(numberAruco), contourVertexes[1],
                             cv2.FONT_HERSHEY_COMPLEX, 1, (100, 0, 255), 2)
    if show:
        cv2.destroyWindow('Aruco')
        cv2.drawContours(imgContours, arucoContours, -1, (0, 0, 255), 1)
        showImage(imgContours)
    return dictAruco


def getMarkupPositions(img, squareRange=[0, 120], show=False):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imgBinary = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(imgBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    markupContours = [cnt for cnt in contours if squareRange[0] < cv2.contourArea(cnt) < squareRange[1]]
    if not markupContours: return []
    markupArray = [findContourCenter(cnt) for cnt in markupContours]
    if show:
        imgContours = img.copy()
        cv2.drawContours(imgContours, markupContours, -1, (255, 0, 0), 1)
        [cv2.putText(imgContours, str(i), (center[0] - 4, center[1] - 4), cv2.FONT_HERSHEY_COMPLEX, 0.3, (100, 0, 255),
                     0)
         for i, center in enumerate(markupArray)]
        showImage(imgContours)
    return markupArray


@lru_cache(maxsize=200)
def getDistanceBetweenPoints(point1, point2):
    return hypot(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))


def minDistanceBetweenLines(line1, line2):
    return min([getDistanceBetweenPoints(point1, point2) for point1 in line1 for point2 in line2])


def showLines(img, lines):
    imgLines = img.copy()
    colorA = (0, 0, 255)
    colorB = (0, 100, 255)
    isA = True
    for line in lines:
        for i in range(len(line) - 1):
            if isA:
                color = colorA
            else:
                color = colorB
            isA = not isA
            cv2.line(imgLines, line[i], line[i + 1], color, 2)
    showImage(imgLines)


def getRoadLines(img, points, show=False):
    # кластеризация точек
    ACCURATE = 1.2  # для baseDistance

    roadLines = []
    sortedPoints = sorted(points)
    baseDistance = min(
        [getDistanceBetweenPoints(sortedPoints[0], sortedPoints[i]) for i in range(1, len(sortedPoints))])
    sortedPoints = sorted(sortedPoints, key=lambda x: getDistanceBetweenPoints(sortedPoints[0], x))
    while sortedPoints:
        start = sortedPoints.pop()
        roadLines += [[start]]
        leftAdd, rightAdd = True, True
        while leftAdd or rightAdd:
            leftAdd, rightAdd = False, False
            left = roadLines[-1][0]
            right = roadLines[-1][-1]
            for i in range(len(sortedPoints) - 1, -1, -1):
                cur = sortedPoints[i]
                if not leftAdd and getDistanceBetweenPoints(left, cur) < baseDistance * ACCURATE:
                    roadLines[-1].insert(0, sortedPoints.pop(i))
                    leftAdd = True
                elif not rightAdd and getDistanceBetweenPoints(right, cur) < baseDistance * ACCURATE:
                    roadLines[-1].append(sortedPoints.pop(i))
                    rightAdd = True
                elif leftAdd and rightAdd:
                    break
    if show:
        showLines(img, roadLines)
    return roadLines


def getDeterminant(a, b):
    return a[0] * b[1] - a[1] * b[0]


def lineIntersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
    div = getDeterminant(xdiff, ydiff)
    if div == 0: return False, None
    d = (getDeterminant(*line1), getDeterminant(*line2))
    x = getDeterminant(d, xdiff) / div
    y = getDeterminant(d, ydiff) / div
    return True, (round(x), round(y))


def drawWayBySampleOutput(img):
    imgCopy = img.copy()
    n = int(input())
    arr = [list(map(int, input().split())) for _ in range(n)]
    for i, pos in enumerate(arr):
        for pos2 in arr[:i]: cv2.circle(imgCopy, pos2, 5, (100, 100, 0), 2)
        cv2.circle(imgCopy, pos, 5, (255, 255, 0), 2)
        showImage(imgCopy)


def drawWayByResultOutput(img, arr, mainPoints, dictAruco):
    imgCopy = img.copy()
    for point in mainPoints:
        pos = point['coordinates'] if 'coordinates' in point else dictAruco[f"p_{point['marker_id']}"]
        cv2.circle(imgCopy, pos, 5, (0, 255, 255), 2)
        cv2.putText(imgCopy, point['name'].split('_')[1], (pos[0] - 10, pos[1] - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                    (100, 0, 255), 2)
    for i, pos in enumerate(arr):
        for pos2 in arr[:i]: cv2.circle(imgCopy, pos2, 5, (100, 100, 0), 2)
        cv2.circle(imgCopy, pos, 5, (255, 255, 0), 2)
        showImage(imgCopy)


def drawMainPoints(img, mainPoints, dictAruco):
    imgCopy = img.copy()
    for point in mainPoints:
        pos = point['coordinates'] if 'coordinates' in point else dictAruco[f"p_{point['marker_id']}"]
        cv2.circle(imgCopy, pos, 5, (0, 255, 255), 2)
        cv2.putText(imgCopy, point['name'].split('_')[1], (pos[0] - 10, pos[1] - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                    (100, 0, 255), 2)
    showImage(imgCopy)


def getUnitVector(point1, point2):
    return [(point2[axis] - point1[axis]) / getDistanceBetweenPoints(point1, point2) for axis in range(2)]


# удлинняем линии на k межточечных расстояния
def extendLines(lines, k=2):
    extendLines = []

    distance = getDistanceBetweenPoints(lines[0][0], lines[0][1]) * k
    for line in lines:
        # продлеваем конец линии
        unitVector = getUnitVector(line[-2], line[-1])
        x, y = distance * unitVector[0] + line[-1][0], distance * unitVector[1] + line[-1][1]
        line.append((ceil(x), ceil(y)))
        # продлеваем начало линии
        vector = getUnitVector(line[1], line[0])
        x, y = line[0][0] + distance * vector[0], line[0][1] + distance * vector[1]
        line.insert(0, (ceil(x), ceil(y)))

        extendLines.append(line)
    return extendLines

def escalatedLines(lines, k=2):
    curLines = lines.copy()
    for count in range(k):
        newLines = [[] for _ in range(len(curLines))]
        for indLine, line in enumerate(curLines):
            for indPoint, point in enumerate(line[:-1]):
                nextPoint = curLines[indLine][indPoint+1]
                newLines[indLine].append(point)
                centerPoint = (int((point[0] + nextPoint[0]) / 2), int((point[1] + nextPoint[1]) / 2))
                newLines[indLine].append(centerPoint)
            newLines[indLine].append(line[-1])
        curLines = newLines.copy()
    return curLines

class Line:
    def __init__(self, id, startPos=None, endPos=None):
        self.id = id
        self.startPos = startPos
        self.endPos = endPos
        self.points = []

    def addPoint(self, point):
        if not self.startPos:
            self.startPos = point
        self.endPos = point
        self.points.append(point)


class Point:
    def __init__(self, id, pos, line=None, isCrossroad=False, isAruco=False, neighbours=[]):
        self.id = id
        self.pos = pos
        self.line = line
        self.isCrossroad = isCrossroad
        self.isAruco = isAruco
        self.isEnd = False
        if not neighbours:
            self.neighbours = []
        else:
            self.neighbours = neighbours

    def addNeighbour(self, point):
        self.neighbours.append(point)

    def isNeighbour(self, point):
        return point in self.neighbours

    def merge(self, point):  # Слияние двух точек (перекрестков)
        self.pos = ((self.pos[0] + point.pos[0]) // 2, (self.pos[1] + point.pos[1]) // 2)
        self.neighbours += point.neighbours


def addCrossroads(img, points, lines, dist, show=False):
    # PS тут много квадратичных сложностей, но концов точек меньше 200 штук, а перекрестков еще меньше
    # поэтому можно не париться

    startsEndsPoints = []
    for line in lines.values():
        startsEndsPoints.append(line.startPos)
        startsEndsPoints.append(line.endPos)

    # minDistBetweenLines = float('+inf')
    # for point1, point2 in combinations(startsEndsPoints, 2):
    #     minDistBetweenLines = min(getDistanceBetweenPoints(point1.pos, point2.pos), minDistBetweenLines)
    minRoadDist = float('+inf')
    for line in lines.values():
        if getDistanceBetweenPoints(line.points[0].pos, line.points[-1].pos) > dist:
            minRoadDist = min(minRoadDist, getDistanceBetweenPoints(line.points[0].pos, line.points[-1].pos))

    crossroads = []
    while startsEndsPoints:
        query = [startsEndsPoints.pop()]
        crossroad = []
        while query:
            point = query.pop()
            crossroad += [point]
            for i in range(len(startsEndsPoints) - 1, -1, -1):
                point2 = startsEndsPoints[i]
                if getDistanceBetweenPoints(point.pos, point2.pos) < minRoadDist * 0.9995:
                    query.append(point2)
                    startsEndsPoints.pop(i)

        # Если 2 точки приналежат одной линии, то выбираем ту, которая ближе к остальным точкам
        # for point1 in crossroad:
        #     for point2 in crossroad:
        #         if point1 == point2: continue
        #         elif point1.line == point2.line:
        #             dist1 = sum([getDistanceBetweenPoints(point1.pos, point.pos) for point in crossroad])
        #             dist2 = sum([getDistanceBetweenPoints(point2.pos, point.pos) for point in crossroad])
        #             if dist1 < dist2:
        #                 crossroad.remove(point1)
        #             else:
        #                 crossroad.remove(point2)
        crossroads.append(crossroad)

    crossroadId = len(points) + 10000
    newCrossroads = []
    for crossroad in crossroads:
        x = round(sum([point.pos[0] for point in crossroad]) / len(crossroad))
        y = round(sum([point.pos[1] for point in crossroad]) / len(crossroad))
        pos = (x, y)
        point = Point(crossroadId, pos, isCrossroad=True, neighbours=crossroad)
        points[crossroadId] = point

        for p in crossroad:
            p.addNeighbour(point)

        crossroadId += 1
        newCrossroads.append(point)
    crossroads = newCrossroads

    # Если расстояние между 2 центрами меньше минимальной длины принадлежащих им линий, то соединяем их в один перекресток
    # to_merge = []
    # for point1 in crossroads:
    #     for point2 in crossroads:
    #         if point1 == point2 or getDistanceBetweenPoints(point1.pos, point2.pos) > 20: continue
    #         minDistance = float('+inf')
    #         for neighbour in point1.neighbours + point2.neighbours:
    #             dist = getDistanceBetweenPoints(neighbour.line.startPos.pos, neighbour.line.endPos.pos)
    #             minDistance = min(minDistance, dist)
    #         if minDistance * 1.1 > getDistanceBetweenPoints(point1.pos, point2.pos):
    #             to_merge.append((point1, point2))

    # print(to_merge)
    # for point1, point2 in to_merge:
    #     point1.merge(point2)
    #     points.pop(point2.id)
    #     crossroads.remove(point2)

    if show:
        imgLines = img.copy()
        for line in lines.values():
            for i in range(len(line.points) - 1):
                cv2.line(imgLines, line.points[i].pos, line.points[i + 1].pos, (0, 0, 255), 2)
        for point in points.values():
            if point.isCrossroad:
                cv2.circle(imgLines, point.pos, 5, (255, 255, 0), 2)
        showImage(imgLines)

    # # Удаляем крайние точки линий
    # print(len(points))
    # for line in lines.values():
    #     p1 = line.points.pop(0)
    #     p2 = line.points.pop(-1)
    #     line.startPos = line.points[0]
    #     line.endPos = line.points[-1]

    #     points.pop(p1.id)
    #     points.pop(p2.id)

    #     for point in p1.neighbours:
    #         point.neighbours.remove(p1)
    #         for point2 in p1.neighbours:
    #             if point2 == point: continue
    #             if point2 not in point.neighbours:
    #                 point.neighbours.append(point2)
    #                 point2.neighbours.append(point)
    #     for point in p2.neighbours:
    #         point.neighbours.remove(p2)
    #         for point2 in p2.neighbours:
    #             if point2 == point: continue
    #             if point2 not in point.neighbours:
    #                 point.neighbours.append(point2)
    #                 point2.neighbours.append(point)

    # print(len(points))

    return points


def getGraph(img, lines, distCros=20, show=False):
    # Рефакторим данные, тк на данном этапе требуется двухсторонняя связь
    points = {}
    newLines = {}
    idLines = 0
    idPoints = 0
    for line in lines:
        newLine = Line(idLines)
        isFirst = True
        for pos in line:
            point = Point(idPoints, pos, newLine)
            points[idPoints] = point
            newLine.addPoint(point)
            if not isFirst:
                points[idPoints - 1].addNeighbour(point)
                point.addNeighbour(points[idPoints - 1])
            idPoints += 1
            isFirst = False
        newLines[idLines] = newLine
        idLines += 1
    lines = newLines

    points = addCrossroads(img, points, lines, distCros, show=show)

    for line in lines.values():
        line.endPos.isEnd = True
        line.startPos.isEnd = True

    return points


# def getGraph(img, roadLines, deviationLen, show=False):
#     notations, mergeList = {}, {}
#     numPoint = 0
#     for line in roadLines:
#         for id in range(len(line)-1):
#             if f'p_{numPoint}' not in mergeList: mergeList[f'p_{numPoint}'] = [f'p_{numPoint+1}']
#             else: mergeList[f'p_{numPoint}'].append(f'p_{numPoint+1}')
#             mergeList[f'p_{numPoint+1}'] = [f'p_{numPoint}']
#             notations[f'p_{numPoint}'] = line[id]
#             numPoint += 1
#         notations[f'p_{numPoint}'] = line[-1]
#         numPoint += 1

# notation - словарь точек и их координат
# mergeList - список смежности

# endPoints = [key for key in mergeList if len(mergeList[key]) == 1]
# crossroads = [[endPoints.pop(0)]]
# id = 0
# while endPoints:
#     for i, plenty in enumerate(crossroads):
#         if all(getDistanceBetweenPoints(notations[endPoints[id]], notations[point]) < deviationLen for point in plenty):
#             crossroads[i].append(endPoints.pop(0))
#             break
#     else: crossroads.append([endPoints.pop(0)])
# if show:
#     for area in crossroads:
#         imgCross = img.copy()
#         [cv2.circle(imgCross, notations[point], 2, (255, 255, 0), 2) for point in area]
#         showImage(imgCross)

def getPosRightSideSegment(img, startPosLine, endPosLine, deviationLen=60, show=False):
    if show: imgCopy = img.copy()
    if startPosLine[0] < 20 or endPosLine[0] < 20:
        print(startPosLine, endPosLine)
    vectorAB = [(endPosLine[axis] - startPosLine[axis]) for axis in range(2)]
    lengthVector = hypot(abs(vectorAB[0]), abs(vectorAB[1]))
    centerPoint = ((startPosLine[0] + endPosLine[0]) / 2, (startPosLine[1] + endPosLine[1]) / 2)
    if lengthVector > 0:
        resultVector = [(deviationLen * vectorAB[1]) / lengthVector,
                        (deviationLen * vectorAB[0]) / lengthVector]
    else:
        resultVector = [0, 0]
    for pr in [1, -1]:
        angles = getAngleBetweenLineAndAxis((startPosLine, endPosLine))
        needPosX, needPosY = (resultVector[0] * pr), (resultVector[1] * pr)
        if angles['x'] > 0 and angles['y'] > 0:
            needPosX, needPosY = needPosX * 1, needPosY * -1
        elif angles['x'] < 0 and angles['y'] > 0:
            needPosX, needPosY = needPosX * 1, needPosY * -1
        elif angles['x'] < 0 and angles['y'] < 0:
            needPosX, needPosY = needPosX * 1, needPosY * -1
        elif angles['x'] > 0 and angles['y'] < 0:
            needPosX, needPosY = needPosX * -1, needPosY * 1
        needPos = (round(centerPoint[0] + needPosX), round(centerPoint[1] + needPosY))
        vectorAC = [(needPos[axis] - startPosLine[axis]) for axis in range(2)]
        deviation = vectorAB[0] * vectorAC[1] - vectorAB[1] * vectorAC[0]
        if deviation > 0:
            if show:
                print(degrees(angles['x']), degrees(angles['y']))
                cv2.line(imgCopy, startPosLine, endPosLine, (130, 130, 0), 2)
                cv2.line(imgCopy, startPosLine, (startPosLine[0], startPosLine[1] + 10), (70, 70, 0), 1)
                cv2.line(imgCopy, startPosLine, (startPosLine[0] + 10, startPosLine[1]), (70, 70, 0), 1)
                cv2.circle(imgCopy, needPos, 5, (255, 255, 0), 2)
                showImage(imgCopy)
            return needPos
    return (ceil(centerPoint[0]), ceil(centerPoint[1]))


def findPathBFS(graph, start, end):
    queue = [(start, [start])]
    while queue:
        vertex, path = queue.pop(0)
        for nxt in vertex.neighbours:
            if nxt in path: continue
            if nxt == end:
                return path + [nxt]
            else:
                queue.append((nxt, path + [nxt]))
    return None


def show_graph(img, points):
    imgLines = img.copy()
    # рисуем граф
    for point in points.values():
        for neighbour in point.neighbours:
            cv2.circle(imgLines, point.pos, 33, (161, 115, 72), 2)
            cv2.line(imgLines, point.pos, neighbour.pos, (76, 235, 23), 2)

    showImage(imgLines)


# Создаем направленный граф
def refactorGraph(img, points, show=False):
    crossroads = list(filter(lambda p: p.isCrossroad, points.values()))
    newPoints = {}
    congruence = {}
    idInt = 0
    for crossroad in crossroads:
        newCrossroad = Point(idInt, crossroad.pos, isCrossroad=True)
        newPoints[idInt] = newCrossroad
        congruence[crossroad.id] = newCrossroad
        idInt += 1

    for crossroad in crossroads:
        newCrossroad = congruence[crossroad.id]
        for point in crossroad.neighbours:
            last = crossroad
            cur = point
            lastNewPoint = newCrossroad
            first = True
            while True:
                if cur.isCrossroad:
                    lastNewPoint.addNeighbour(congruence[cur.id])
                    break
                if not first:
                    newPos = getPosRightSideSegment(img, last.pos, cur.pos, show=False)
                else:
                    newPos = cur.pos
                    first = False
                newPoint = Point(idInt, newPos)
                lastNewPoint.addNeighbour(newPoint)
                newPoints[idInt] = newPoint
                idInt += 1
                if cur.isCrossroad:
                    break
                for nxt in cur.neighbours:
                    if nxt != last:
                        last = cur
                        cur = nxt
                        lastNewPoint = newPoint
                        break

    if show:
        imgLines = img.copy()
        # рисуем перекрестки
        for point in newPoints.values():
            if point.isCrossroad:
                cv2.circle(imgLines, point.pos, 5, (255, 255, 0), 2)
        show_graph(imgLines, newPoints)

    return newPoints


def addArucos(img, points, arucos, mainPoints, show=False):
    acucoId2PointId = {}
    for point in mainPoints:
        if "marker_id" in point:
            acucoId2PointId[f'p_{point["marker_id"]}'] = point["name"]

    pointsList = list(points.values())
    for arucoId, aruco in arucos.items():
        pointsList.sort(key=lambda p: getDistanceBetweenPoints(p.pos, aruco))
        # Берем 3 точки, сортируем по ходу движения
        closest = pointsList[:3]
        first = closest
        for i in closest:
            for neighbour in i.neighbours:
                if neighbour in closest:
                    first.remove(neighbour)
        first = first[0]
        closest2 = [first]
        for i in range(2):
            closest2.append(closest2[-1].neighbours[0])
        closest = closest2
        if arucoId in acucoId2PointId:
            pointId = acucoId2PointId[arucoId]
        else:
            pointId = f'p_{arucoId}'
        arucoPoint = Point(pointId, aruco, isAruco=True, neighbours=[closest[2]])
        points[pointId] = arucoPoint
        closest[0].addNeighbour(arucoPoint)

    if show:
        img = img.copy()
        show_graph(img, points)

    return points


def addPoints(img, points, addPoints, show=False):
    pointsList = list(points.values())
    for pointData in addPoints:
        if "coordinates" in pointData and pointData["name"] not in points:
            pointsList.sort(key=lambda p: getDistanceBetweenPoints(p.pos, tuple(pointData["coordinates"])))
            closest = pointsList[0]
            if closest.isCrossroad:
                newPoint = Point(pointData["name"], tuple(pointData["coordinates"]), neighbours=[closest])
                points[pointData["name"]] = newPoint
                closest.addNeighbour(newPoint)
            else:
                closest.pos = tuple(pointData["coordinates"])
                points.pop(closest.id)
                closest.id = pointData["name"]
                points[pointData["name"]] = closest

    if show:
        img = img.copy()
        # рисуем граф
        show_graph(img, points)

    return points


def getResultPositions(graph, robotPos, mainPoints):
    plist = list(graph.values())
    plist.sort(key=lambda p: getDistanceBetweenPoints(p.pos, tuple(robotPos)))
    start = plist[0]
    mainPoints = [i["name"] for i in mainPoints]
    last = start
    resultPositions = [start.pos]
    for point in mainPoints:
        point = graph[point]
        path = findPathBFS(graph, last, point)
        last = point
        resultPositions += [p.pos for p in path[1:]]
    return resultPositions


def debug():
    from modules.utils import getSampleData
    numEx = 2
    imageString, robotPos, countPoints, mainPoints = getSampleData(numEx)

    img = cv2.imread("maps/final.png")


    # buffer = base64.b64decode(imageString)
    # array = np.frombuffer(buffer, dtype=np.uint8)
    # img = cv2.imdecode(array, flags=1)

    # nameImgFile = f'maps/map{numEx}.png'
    # if 'maps' in os.listdir() and nameImgFile not in os.listdir('maps'): cv2.imwrite(nameImgFile, img)

    # drawWayBySampleOutput(img)

    # Get data
    dictAruco = detectAruco(img, 3, show=False)
    markupArray = getMarkupPositions(img, show=True)
    roadLines = getRoadLines(img, markupArray, show=True)
    escalatedRoadLines = escalatedLines(roadLines, k=1)
    showLines(img, escalatedRoadLines)
    extendedRoadLines = extendLines(roadLines)
    showLines(img, extendedRoadLines)

    print(dictAruco)
    print(markupArray)
    print(roadLines)

    # drawMainPoints(img, mainPoints, dictAruco)

    graph = getGraph(img, extendedRoadLines, show=True)
    graph = refactorGraph(img, graph, show=True)
    # graph = addArucos(img, graph, dictAruco, mainPoints, show=True)
    # graph = addPoints(img, graph, mainPoints, show=True)

    resultPositions = getResultPositions(graph, robotPos, [])

    cv2.circle(img, (1513, 545), 5, (0, 255, 0))
    showImage(img)

    drawWayByResultOutput(img, resultPositions, [], dictAruco)

    # print(len(resultPositions))
    # [print(*pos) for pos in resultPositions]

    cv2.destroyAllWindows()


def main():
    img, robotPos, countPoints, mainPoints = readInput()

    # Get data
    dictAruco = detectAruco(img, 3)
    markupArray = getMarkupPositions(img)
    roadLines = getRoadLines(img, markupArray)
    #escalatedRoadLines = escalatedLines(roadLines, k=0)
    extendedRoadLines = extendLines(roadLines)

    graph = getGraph(img, extendedRoadLines)
    graph = refactorGraph(img, graph)
    graph = addArucos(img, graph, dictAruco, mainPoints)
    graph = addPoints(img, graph, mainPoints)

    resultPositions = [tuple(robotPos)] + getResultPositions(graph, robotPos, mainPoints)

    print(len(resultPositions))
    [print(*pos) for pos in resultPositions]


if __name__ == '__main__':
    # adjustPath(__file__)
    debug()
    #main()