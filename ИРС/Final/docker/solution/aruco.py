import time

import cv2
from cv2 import aruco
from funcs import *
from vision import showImage

ALL_ARUCO_KEYS = [1, 2, 3, 5, 6, 7, 10, 11, 12, 13, 14, 15, 17, 18, 19, 21, 22, 23, 26, 27, 28, 29, 30, 31, 33, 35, 37,
                  39, 41, 42, 43, 44, 45, 46, 47, 49, 51, 53, 55, 57, 58, 59, 60, 61, 62, 63, 69, 70, 71, 76, 77, 78,
                  79, 85, 86, 87, 92, 93, 94, 95, 97, 98, 99, 101, 102, 103, 105, 106, 107, 109, 110, 111, 113, 114,
                  115, 117, 118, 119, 121, 122, 123, 125, 126, 127, 141, 142, 143, 157, 158, 159, 171, 173, 175, 187,
                  189, 191, 197, 199, 205, 206, 207, 213, 215, 221, 222, 223, 229, 231, 237, 239, 245, 247, 253, 255,
                  327, 335, 343, 351, 367, 383]

class ArucoDetector:
    def __init__(self, size, whitelist):
        self.size = size
        self.whitelist = whitelist
        self.dictionary = aruco.Dictionary(np.empty(shape=(384, 2, 4), dtype=np.uint8), size)
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

def showDetectedMarkers(img, markerCorners, markerIds):
    imgShow = img.copy()
    aruco.drawDetectedMarkers(imgShow, markerCorners)
    for cnr, id in zip(markerCorners, markerIds):
        pos = list(map(int, list(cnr[0][0])))
        cv2.putText(imgShow, str(id), pos, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    showImage(imgShow)
    showImage(cv2.cvtColor(imgShow, cv2.COLOR_BGR2GRAY))

def findArucoMarkers(camera, size=3, timer=2, blockSize=73, C=14, sizeBlur=2, show=False):
    detector = ArucoDetector(size, whitelist=ALL_ARUCO_KEYS)
    lastTime = time.time()
    markerDict = {}
    while lastTime + timer > time.time():
        imgGray = cv2.cvtColor(camera.read(), cv2.COLOR_BGR2GRAY)
        imgBinary = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, C)
        imgBinary = cv2.blur(imgBinary, (sizeBlur, sizeBlur))
        markerCorners, markerIds = detector.detectMarkers(imgBinary)
        for cnr, id in zip(markerCorners, markerIds): markerDict[id[0]] = cnr
    markerCorners, markerIds = list(markerDict.values()), list(markerDict.keys())
    if show:
        showImage(imgBinary)
        showDetectedMarkers(camera.read(), markerCorners, markerIds)
    return markerCorners, markerIds

def detectAruco(img, markerCorners, markerIds, threshold, size=3):
    resultArucos = {}
    for cnr, id in zip(markerCorners, markerIds):
        corners = np.array(list(map(np.array, cnr[0])))
        imgWrapped = fourPointTransform(img, corners)
        imgWGray = cv2.cvtColor(imgWrapped, cv2.COLOR_BGR2GRAY)
        matrix = getMatrixFromAruco(imgWGray, threshold, size)
        centerX = sum([i[0] for i in corners]) / 4
        centerY = sum([i[1] for i in corners]) / 4
        a, b = list(sorted(corners, key=lambda x: x[1]))[:2]
        if b[0] < a[0]:
            c = [a[0] + 5, a[1]]
            angle = 1
        else:
            c = [a[0] - 5, a[1]]
            angle = -1
        angle *= math.degrees(getAngleBetweenLines([b, a], [a, c]))
        for n in range(5):
            markerId = 0
            for i in range(9):
                x = i % 3
                y = i // 3
                markerId += matrix[y][x] * 2 ** (8 - i)
            if markerId in ALL_ARUCO_KEYS:
                angle += n * 90
                if angle < 0: angle += 360
                resultArucos[f"p_{id}"] = ((centerX, centerY), math.radians(angle))
                break
            matrix = rotateMatrix(matrix)
    return resultArucos

def getMatrixFromAruco(imgGray, threshold, sizeAruco):
    height, width = imgGray.shape[:2]
    stepH, stepW = height // (sizeAruco + 1), width // (sizeAruco + 1)
    matrix = [[0] * sizeAruco for _ in range(sizeAruco)]
    for i in range(1, sizeAruco + 1):
        for j in range(1, sizeAruco + 1):
            y = stepH * i
            x = stepW * j
            matrix[i - 1][j - 1] = int(imgGray[y][x] > threshold)
    return matrix


