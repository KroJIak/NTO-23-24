import math
from typing import List

import numpy as np
import cv2
import json
import traceback


def save():
    resultMapDict = mapDict.copy()
    for key, pnt in mapDict['notations'].items(): resultMapDict['notations'][key] = pointToDict(pnt)
    with open('map.json', 'w', encoding='utf-8') as file:
        json.dump(resultMapDict, file, indent=4, ensure_ascii=False)

def pointToDict(point):
    dictPoint = dict(id=point.id,
                     pos=point.pos,
                     isCrossroad=point.isCrossroad,
                     isAruco=point.isAruco)
    return dictPoint


class Window:
    def __init__(self, mainImg, offset, nameWindow='SceneImage'):
        self.mainImg = mainImg
        self.offset = offset
        self.nameWindow = nameWindow
        self.sceneImg = self.createSceneImage()
        self.insertMainImage()

        self.countPoints = 0
        self.drawMode = True # True - points; False - lines
        self.pointMode = 0 # 0 - road; 1 - crossroad; 2 - aruco
        self.startLine = None

        self.roadColor = (0, 200, 0)
        self.crossroadColor = (130, 170, 10)
        self.arucoColor = (0, 0, 200)
        self.lineColor = (150, 100, 100)

        self.show()
        cv2.setMouseCallback(nameWindow, self.checkMouse)

    def createSceneImage(self, color=80):
        height, width = self.mainImg.shape[:2]
        img = np.zeros((height+self.offset*2, width+self.offset*2, 3), dtype=np.uint8)
        img[:, :, :] = color
        return img

    def insertMainImage(self):
        self.sceneImg[self.offset:self.offset+self.mainImg.shape[0],
                      self.offset:self.offset+self.mainImg.shape[1]] = self.mainImg

    def show(self):
        resultImg = self.sceneImg.copy()
        resultImg = self.drawPoints(resultImg)
        resultImg = self.drawLines(resultImg)
        cv2.imshow(self.nameWindow, resultImg)
        self.checkKeys()

    def drawPoints(self, img, radius=5):
        resultImg = img.copy()
        for id, pnt in mapDict['notations'].items():
            if pnt.isAruco: color = self.arucoColor
            elif pnt.isCrossroad: color = self.crossroadColor
            else: color = self.roadColor
            resultPos = pnt.pos[0] + self.offset, pnt.pos[1] + self.offset
            cv2.circle(resultImg, resultPos, radius+2, (255, 255, 255), -1)
            cv2.circle(resultImg, resultPos, radius, color, -1)
        return resultImg

    def drawLines(self, img, thickness=3):
        resultImg = img.copy()
        for startId, neighbors in mapDict['graph'].items():
            startPoint = mapDict['notations'][startId]
            startPos = list(map(lambda x: x + self.offset, startPoint.pos))
            for endId in neighbors:
                endPoint = mapDict['notations'][endId]
                endPos = list(map(lambda x: x + self.offset, endPoint.pos))
                cv2.arrowedLine(resultImg, startPos, endPos, self.lineColor, thickness)
        return resultImg

    def checkKeys(self):
        key = cv2.waitKey(1)
        match key:
            case 27: # Esc
                exit(0)
            case 32: # Space
                self.drawMode = not self.drawMode
                self.startLine = None
            case 97: # A
                self.pointMode = 0
            case 115: # S
                self.pointMode = 1
            case 100: # D
                self.pointMode = 2

    def checkMouse(self, event, x, y, flags, param):
        realPos = (x-self.offset, y-self.offset)
        if not (0 <= realPos[0] < self.mainImg.shape[1] and 0 <= realPos[1] < self.mainImg.shape[0]): return
        match event:
            case cv2.EVENT_LBUTTONDOWN:
                if self.drawMode:
                    self.countPoints += 1
                    addPoint(self.countPoints, realPos, self.pointMode)
                else:
                    if not self.startLine and self.countPoints > 0:
                        self.startLine = getNearestPoints(realPos)[0]
                    elif self.startLine:
                        nearestPoints = getNearestPoints(realPos)
                        nearestPoints.pop(nearestPoints.index(self.startLine))
                        endLine = nearestPoints[0]
                        addLine(self.startLine, endLine)
                        self.startLine = None
            case cv2.EVENT_MBUTTONDOWN:
                if self.drawMode and self.countPoints > 0:
                    removeNearestPoint(realPos)
                    if not len(mapDict['notations']): self.countPoints = 0
                    else: self.countPoints = max(mapDict['notations'].keys())
                else:
                    countConnections = sum(list(map(len, mapDict['graph'].values())))
                    if countConnections > 0:
                        removeNearestLine(realPos)

class Point:
    def __init__(self, id: int, pos: List[int], isCrossroad=False, isAruco=False):
        self.id = id
        self.pos = pos
        self.isCrossroad = isCrossroad
        self.isAruco = isAruco

def distanceBetweenPos(pos1, pos2):
    dist = math.hypot(pos1[0]-pos2[0], pos1[1]-pos2[1])
    return dist

def getNearestPoints(targetPos):
    allPoints = list(mapDict['notations'].values())
    nearestPoints = sorted(allPoints, key=lambda pnt: distanceBetweenPos(targetPos, pnt.pos))
    return nearestPoints

def addPoint(id, pos, mode):
    isCrossroad = True if mode == 1 else False
    isAruco = True if mode == 2 else False
    resultPoint = Point(id, pos, isCrossroad, isAruco)
    mapDict['notations'][id] = resultPoint

def removeNearestPoint(pos):
    nearestPoint = getNearestPoints(pos)[0]
    changedGraph = mapDict['graph'].copy()
    if nearestPoint.id in changedGraph:
        del changedGraph[nearestPoint.id]
    for startId, neighbors in mapDict['graph'].items():
        if nearestPoint.id in neighbors:
            changedGraph[startId].pop(changedGraph[startId].index(nearestPoint.id))
            if not len(changedGraph[startId]):
                del changedGraph[startId]
    mapDict['graph'] = changedGraph
    del mapDict['notations'][nearestPoint.id]

def removeNearestLine(pos):
    startPoint, endPoint = getNearestPoints(pos)[:2]
    for i in range(2):
        if startPoint.id in mapDict['graph'] and endPoint.id in mapDict['graph'][startPoint.id]:
            mapDict['graph'][startPoint.id].pop(mapDict['graph'][startPoint.id].index(endPoint.id))
            if not len(mapDict['graph'][startPoint.id]):
                del mapDict['graph'][startPoint.id]
        startPoint, endPoint = endPoint, startPoint

def addLine(startPoint, endPoint):
    if startPoint.id not in mapDict['graph']:
        mapDict['graph'][startPoint.id] = [endPoint.id]
    else:
        mapDict['graph'][startPoint.id].append(endPoint.id)

# CONST
OFFSET = 50
mapDict = dict(graph={}, notations={})

def main():
    inputImg = cv2.imread('splice.png')
    window = Window(inputImg, offset=OFFSET)
    while True: window.show()

if __name__ == '__main__':
    try: main()
    except SystemExit: pass
    except: traceback.print_exc()
    finally: save()