import time

import numpy as np
import cv2
from cv2 import aruco

ALL_ARUCO_KEYS = [7, 10]

# класс-детектор для обнаружения aruco меток размера 3x3
class ArucoDetector:
    def __init__(self, size, whitelist):
        self.size = size
        self.whitelist = whitelist
        self.dictionary = aruco.Dictionary(np.empty(shape=(max(ALL_ARUCO_KEYS)+1, 2, 4), dtype=np.uint8), size)
        self.fillDictionary()
        self.parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.dictionary, self.parameters)

    def getBits(self, id):
        binId = bin(id)[2:].rjust(self.size**2, '0')
        bits = np.array(list(binId), dtype=np.uint8).reshape(-1, self.size)
        return bits

    def fillDictionary(self):
        for id in self.whitelist:
            bits = self.getBits(id)
            self.dictionary.bytesList[id] = aruco.Dictionary.getByteListFromBits(bits)

    def detectMarkers(self, imgGray):
        rawMarkerCorners, rawMarkerIds, rejectedCandidates = self.detector.detectMarkers(imgGray)
        markerCorners, markerIds = [], []
        if rawMarkerIds is None: return [], []
        for i, id in enumerate(rawMarkerIds):
            if id in self.whitelist:
                markerCorners.append(rawMarkerCorners[i])
                markerIds.append(rawMarkerIds[i])
        return markerCorners, markerIds

# получить центр aruco метки
def getArucoCenter(corners):
    centerX, centerY = 0, 0
    for pos in corners:
        centerX += pos[0]
        centerY += pos[1]
    center = (centerX / len(corners), centerY / len(corners))
    return center

# вывести найденные aruco метки на экране
def showDetectedMarkers(img, markerCorners, markerIds):
    imgShow = img.copy()
    aruco.drawDetectedMarkers(imgShow, markerCorners)
    for cnr, id in zip(markerCorners, markerIds):
        pos = list(map(int, list(cnr[0][0])))
        cv2.putText(imgShow, str(id), pos, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Aruco', imgShow)

#blockSize=73, C=14, sizeBlur=2,
#imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#imgBinary = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, C)
#imgBinary = cv2.blur(imgBinary, (sizeBlur, sizeBlur))

# основная фукнция обнаружения aruco меток
def detectArucoMarkers(img, size=3, show=False):
    detector = ArucoDetector(size, whitelist=ALL_ARUCO_KEYS)
    markerCorners, markerIds = detector.detectMarkers(img)
    if show: showDetectedMarkers(img, markerCorners, markerIds)
    arucoDict = {id[0]: getArucoCenter(cnr[0]) for id, cnr in zip(markerIds, markerCorners)}
    return arucoDict

# функция для тестирования
def mainAruco():
    cap = cv2.VideoCapture(2)
    while True:
        _, img = cap.read()
        arucoDict = detectArucoMarkers(img, show=True)
        for id, center in arucoDict.items():
            arucoCenterImg = (int(center[0]), int(center[1]))
            cv2.circle(img, arucoCenterImg, 5, (0, 0, 255), -1)
        cv2.imshow('Image', img)
        if cv2.waitKey(1) == 27: break

if __name__ == '__main__':
    mainAruco()
