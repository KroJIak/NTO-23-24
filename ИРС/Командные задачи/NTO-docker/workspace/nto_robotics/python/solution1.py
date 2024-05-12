import sys
import os
import time

from nto_sim.py_nto_task1 import Task
import cv2

import traceback

## Здесь должно работать ваше решение
def solve(task: Task):
    import numpy as np
    from math import radians, degrees, hypot, pi, acos
    from functools import lru_cache
    from collections import deque
    ALL_ARUCO_KEYS = [1, 2, 3, 5, 6, 7, 10, 11, 12, 13, 14, 15, 17, 18, 19, 21, 22, 23, 26, 27, 28, 29, 30, 31, 33, 35,
                      37, 39, 41, 42, 43, 44, 45, 46, 47, 49, 51, 53, 55, 57, 58, 59, 60, 61, 62, 63, 69, 70, 71, 76,
                      77, 78, 79, 85, 86, 87, 92, 93, 94, 95, 97, 98, 99, 101, 102, 103, 105, 106, 107, 109, 110, 111,
                      113, 114, 115, 117, 118, 119, 121, 122, 123, 125, 126, 127, 141, 142, 143, 157, 158, 159, 171,
                      173, 175, 187, 189, 191, 197, 199, 205, 206, 207, 213, 215, 221, 222, 223, 229, 231, 237, 239,
                      245, 247, 253, 255, 327, 335, 343, 351, 367, 383]
    ROBOT_NUM = 0
    VOLTAGES = [0, 0]
    class Motor():
        def __init__(self, robotNum, port):
            self.robotNum = robotNum
            self.port = port
            self.maxVoltage = 25
        def setSpeed(self, percent):
            VOLTAGES[self.port] = (max(-100, min(100, percent)) * self.maxVoltage) / 100
            task.setMotorVoltage(self.robotNum, VOLTAGES)
        def getAngle(self, state):
            if self.port == 0: return radians(state.leftMotorAngle)
            elif self.port == 1: return radians(state.rightMotorAngle)
        def getAngularSpeed(self, state):
            if self.port == 0: return state.leftMotorSpeed
            elif self.port == 1: return state.rightMotorSpeed

    ## Загружаем изображение из задачи
    ## сцена отправляется с определенной частотй
    ## для этого смотри в документацию к задаче
    # mapImage = task.getTaskMap()
    # cv2.imwrite('../data/ex1-map.png', mapImage)
    # countRobots = task.robotsSize()
    # print('Number of robots:', countRobots)
    # state = task.getRobotState(ROBOT_NUM)
    # print("Left Motor angle:", state.leftMotorAngle)
    # print("Right Motor angle:", state.rightMotorAngle)
    # print("Left Motor speed:", state.leftMotorSpeed)
    # print("Right Motor speed:", state.rightMotorSpeed)

    taskInfo = eval(task.getTask())
    print('Task: ', taskInfo)

    M1 = Motor(ROBOT_NUM, 0)
    M2 = Motor(ROBOT_NUM, 1)

    sceneImg = task.getTaskScene()

    def rotateImage(img, rotationPoint, theta, width, height):
        shape = (img.shape[1], img.shape[0])
        matrix = cv2.getRotationMatrix2D(center=rotationPoint, angle=degrees(theta), scale=1)
        resultImg = cv2.warpAffine(src=img, M=matrix, dsize=shape)
        x = int(rotationPoint[0] - width / 2)
        y = int(rotationPoint[1] - height / 2)
        resultImg = resultImg[y:y + height, x:x + width]
        return resultImg

    def showImage(img):
        cv2.imshow('Scene', img)
        key = cv2.waitKey(int(1000 / 30))  # мс
        if key == 27: raise ValueError('Emergency stop')
        # time.sleep(1/30)

    def getAngleBetweenLines(line1, line2):
        startPosLine1, endPosLine1 = line1
        startPosLine2, endPosLine2 = line2
        vector1 = [(endPosLine1[axis] - startPosLine1[axis]) for axis in range(2)]
        vector2 = [(endPosLine2[axis] - startPosLine2[axis]) for axis in range(2)]
        scalarProduct = np.dot(vector1, vector2)
        lengthVector1 = hypot(abs(vector1[0]), abs(vector1[1]))
        lengthVector2 = hypot(abs(vector2[0]), abs(vector2[1]))
        lengthsProduct = lengthVector1 * lengthVector2
        if lengthsProduct == 0 or not (-1 <= (scalarProduct / lengthsProduct) <= 1): return pi
        angle = acos(scalarProduct / lengthsProduct)
        return angle

    def findContourCenter(cnt):
        cx, cy = None, None
        moment = cv2.moments(cnt)
        if moment['m00'] != 0:
            #print(moment['m00'], cv2.contourArea(cnt))
            cx = int(moment['m10'] / moment['m00'])
            cy = int(moment['m01'] / moment['m00'])
        return (cx, cy)

    @lru_cache(maxsize=200)
    def getDistanceBetweenPoints(point1, point2):
        return hypot(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))

    def getPointOnSameLineOnSquare(vertexes, minDist, maxDist):
        limitDist = minDist + (minDist + maxDist) // 2
        for i, pos1 in enumerate(vertexes[:-1]):
            for j, pos2 in enumerate(vertexes[i + 1:]):
                if hypot(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1])) < limitDist:
                    return pos1, pos2

    def detectAruco(img, size, areaRange=[2000, 9000], coefApprox=0.03):
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, imgBinary = cv2.threshold(imgGray, 160, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(imgBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # [print(i, cv2.contourArea(cnt)) for i, cnt in enumerate(sorted(contours, key=cv2.contourArea, reverse=True))]

        arucoContours = [cnt for cnt in contours if areaRange[0] < cv2.contourArea(cnt) < areaRange[1]]
        if not arucoContours: return {}
        dictAruco = {}

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
                                                                      min(allDistBetweenPoints),
                                                                      max(allDistBetweenPoints))
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
            for i in range(4):
                cpArucoArray = arucoArray.copy()
                cpArucoArray.resize(size ** 2)
                numberAruco = int(''.join(list(map(str, cpArucoArray))), 2)
                if numberAruco in ALL_ARUCO_KEYS: break
                arucoArray = np.rot90(arucoArray)
            else: continue
            dictAruco[f'a_{numberAruco}'] = centerContour
        return dictAruco

    def getPointDirectionRobot(img, HSVMin=(62, 214, 255), HSVMax=(133, 255, 255)):
        HSVImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        binaryImg = cv2.inRange(HSVImg, HSVMin, HSVMax)
        contours, _ = cv2.findContours(binaryImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        mainPoints = [findContourCenter(cnt) for cnt in contours]
        allDistance = [getDistanceBetweenPoints(point1, point2) for i, point1 in enumerate(mainPoints[:-1]) for j, point2 in enumerate(mainPoints[i+1:])]
        maxDistance = sorted(allDistance)[-1]
        for i, point1 in enumerate(mainPoints):
            for j, point2 in enumerate(mainPoints):
                if i == j: continue
                if getDistanceBetweenPoints(point1, point2) >= maxDistance:
                    break
            else:
                pointDirection = point1
                break
        return pointDirection

    def getPointCenterRobot(img, HSVMin=(0, 0, 224), HSVMax=(195, 86, 234)):
        HSVImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        binaryImg = cv2.inRange(HSVImg, HSVMin, HSVMax)
        contours, _ = cv2.findContours(binaryImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        sortedContours = sorted(contours, key=cv2.contourArea)
        pointCenter = findContourCenter(sortedContours[-1])
        return pointCenter

    def getErrorByPoints(point1, point2, commonPoint, reverse=True):
        angle = getAngleBetweenLines((point1, commonPoint), (commonPoint, point2))
        vectorAB = [(point1[axis] - commonPoint[axis]) for axis in range(2)]
        vectorAC = [(point2[axis] - commonPoint[axis]) for axis in range(2)]
        deviation = vectorAB[0] * vectorAC[1] - vectorAB[1] * vectorAC[0]
        error = pi - angle if reverse else angle
        if deviation < 0: error *= -1
        return error

    def robotController(speed, error, errOld, kp=1.2, kd=1.7):
        u = kp * error + kd * (error - errOld)
        M1.setSpeed(speed + u)
        M2.setSpeed(speed - u)

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
                    points[i][j] = (points[i][j][0] + deviation[0], points[i][j][1] + deviation[1])
                    continue
                points[i][j] = None
        if show: showImage(copyImg)
        return points
    
    def getNearestPoint(curPoint, dictPoints):
        nearestPoint = None
        minDist = float('inf')
        for pointId, pointPos in dictPoints.items():
            dist = getDistanceBetweenPoints(curPoint, pointPos)
            if dist < minDist:
                minDist = dist
                nearestPoint = pointId
        return nearestPoint

    def getMergeListWithAruco(img, points, taskInfo, dictAruco, show=False):
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
        if show: showImage(copyImg)

        needAruco = [f"a_{point['marker_id']}" for point in taskInfo if 'marker_id' in point]
        for arucoId, arucoPos in dictAruco.items():
            if arucoId not in needAruco: continue
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

    def forwardToPoint(speed, point):
        errOld = 0
        while True:
            sceneImg = task.getTaskScene()
            pointCenter = getPointCenterRobot(sceneImg)
            pointDirection = getPointDirectionRobot(sceneImg)
            distance = getDistanceBetweenPoints(pointCenter, point)
            if distance < 10: break
            error = getErrorByPoints(point, pointDirection, pointCenter)
            robotController(speed, error, errOld)
            errOld = error
            cv2.circle(sceneImg, point, 2, (0, 0, 255), 2)
            showImage(sceneImg)

    def turnToPoint(speed, point, eps=0.15):
        while True:
            sceneImg = task.getTaskScene()
            pointDirection = getPointDirectionRobot(sceneImg)
            pointCenter = getPointCenterRobot(sceneImg)
            angle = getErrorByPoints(point, pointDirection, pointCenter)
            if abs(angle) > pi - eps * 2: nspeed = 1
            else: nspeed = speed
            if abs(angle) > pi - eps: break
            speeds = [-nspeed, nspeed] if angle < 0 else [nspeed, -nspeed]
            M1.setSpeed(speeds[0])
            M2.setSpeed(speeds[1])
            cv2.circle(sceneImg, point, 2, (0, 0, 255), 2)
            showImage(sceneImg)

    sceneImg = task.getTaskScene()

    speed = 50
    slowSpeed = 10
    dictAruco = detectAruco(sceneImg, 3)
    deviation, cutImg = cutMainImage(sceneImg)
    contoursObstacles = getContoursObstacles(cutImg)
    activePoints = getActivePoints(cutImg, deviation, contoursObstacles)
    notation, mergeList = getMergeListWithAruco(sceneImg, activePoints, taskInfo, dictAruco)
    # state = task.getRobotState(ROBOT_NUM)
    for needPoint in taskInfo:
        sceneImg = task.getTaskScene()
        pointCenter = getPointCenterRobot(sceneImg)
        nearestPointByRobot = getNearestPoint(pointCenter, notation)
        print(needPoint)
        if 'marker_id' in needPoint: nearestPointByEndPoint = f"a_{needPoint['marker_id']}"
        else: nearestPointByEndPoint = getNearestPoint(tuple(needPoint['coordinates'][:2]), notation)
        way = bfs(mergeList, nearestPointByRobot, nearestPointByEndPoint)
        turnToPoint(slowSpeed, notation[nearestPointByRobot])
        forwardToPoint(speed, notation[nearestPointByRobot])
        for indPoint, point in enumerate(way):
            curSpeed = speed if indPoint < len(way)-1 else slowSpeed
            turnToPoint(slowSpeed, notation[point])
            forwardToPoint(curSpeed, notation[point])
        if 'coordinates' in needPoint:
            endPoint = tuple(needPoint['coordinates'][:2])
            turnToPoint(slowSpeed, endPoint)
            forwardToPoint(slowSpeed, endPoint)

        


if __name__ == '__main__':
    ## Запуск задания и таймера (внутри задания)
    task = Task()
    task.start()

    try:
        solve(task)
    except Exception as e:
        # traceback.print_exc()
        print(e)

    task.stop()
