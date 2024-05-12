from modules.utils import getSampleData
from cv2 import aruco
import numpy as np
import base64
import cv2
import os

ALL_ARUCO_KEYS = [1, 2, 3, 5, 6, 7, 10, 11, 12, 13, 14, 15, 17, 18, 19, 21, 22, 23, 26, 27, 28, 29, 30, 31, 33, 35, 37, 39, 41, 42, 43, 44, 45, 46, 47, 49, 51, 53, 55, 57, 58, 59, 60, 61, 62, 63, 69, 70, 71, 76, 77, 78, 79, 85, 86, 87, 92, 93, 94, 95, 97, 98, 99, 101, 102, 103, 105, 106, 107, 109, 110, 111, 113, 114, 115, 117, 118, 119, 121, 122, 123, 125, 126, 127, 141, 142, 143, 157, 158, 159, 171, 173, 175, 187, 189, 191, 197, 199, 205, 206, 207, 213, 215, 221, 222, 223, 229, 231, 237, 239, 245, 247, 253, 255, 327, 335, 343, 351, 367, 383]
BLACKLIST_ARUCO = [key for key in range(max(ALL_ARUCO_KEYS)+1) if key not in ALL_ARUCO_KEYS]

def showImage(img):
    while cv2.waitKey(1) != 27: cv2.imshow('Image', img)

def getZero3DImage(shape):
    height, width = shape[:2]
    zeroImg = np.zeros((height, width), dtype=np.uint8)
    zeroImg.fill(255)
    return zeroImg

def detectAruco(img, arucoDict, blacklist=None):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    filter = np.array([[-1, -1, -1], [-1, 15, -1], [-1, -1, -1]])
    imgThresh=cv2.filter2D(imgGray,-1,filter)
    #imgBlur = cv2.blur(imgGray, (3, 3))
    #_, imgThresh = cv2.threshold(imgBlur, 80, 30, cv2.THRESH_BINARY)
    showImage(imgThresh)

    detector = aruco.ArucoDetector(arucoDict,
                                   aruco.DetectorParameters())
    bbox, ids, _ = detector.detectMarkers(imgThresh)
    if blacklist:
        try:
            countPop = 0
            for i, id in enumerate(ids.copy()):
                if id[0] in blacklist:
                    ids = np.concatenate((ids[:i-countPop], ids[i-countPop+1:]), axis=0)
                    print(bbox)
                    bbox = np.concatenate((bbox[:i-countPop], bbox[i-countPop+1:]), axis=0)
                    countPop += 1
        except: pass
    return bbox, ids

def drawAruco(img, bbox, ids):
    if ids is None: return img
    resultImg = img.copy()
    cv2.aruco.drawDetectedMarkers(resultImg, bbox)
    for i in range(len(ids)):
        cv2.putText(resultImg, str(ids[i]), list(map(int, bbox[i][0][0])),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (100, 0, 255), 2)
    return resultImg

def saveAruco(key, arucoDict, show=False, path='ARUCO_3X3_IMAGES'):
    offset = 40
    zeroImg = getZero3DImage((400 + offset * 2, 400 + offset * 2))
    arucoImg = cv2.aruco.generateImageMarker(arucoDict, key, 400)
    zeroImg[offset:offset + arucoImg.shape[0], offset:offset + arucoImg.shape[1]] = arucoImg
    if show: showImage(zeroImg)
    cv2.imwrite(f'{path}/{key}.png', zeroImg)

def createArucoDict(arrKeys, size):
    byteArr = []
    for key in arrKeys:
        digitalNum = bin(key)[2:].rjust(size**2, '0')
        # print(key, digitalNum)
        arr = np.array(list(map(int, list(digitalNum))))
        markerBits = cv2.Mat(arr)
        markerCompressed = cv2.aruco.Dictionary.getByteListFromBits(markerBits)
        byteArr.append(markerCompressed[0])
    bytesList = np.array(byteArr)
    arucoDict = cv2.aruco.Dictionary(bytesList, size, 0)
    return arucoDict


# imageString = input()
# robotPos = list(map(int, input().split()))
# countPoints = int(input())
# mainPoints = eval(input())
numEx = 0
imageString, robotPos, countPoints, mainPoints = getSampleData(numEx)

buffer = base64.b64decode(imageString)
array = np.frombuffer(buffer, dtype=np.uint8)
img = cv2.imdecode(array, flags=1)
nameImgFile = f'maps/map{numEx}.png'
if nameImgFile not in os.listdir('../maps'): cv2.imwrite(nameImgFile, img)

imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
imgBlur = cv2.blur(imgHSV, (1, 1))
imgBinary = cv2.inRange(imgBlur, np.array([0, 0, 199]), np.array([0, 0, 255]))
showImage(img)
showImage(imgBinary)

span = range(max(ALL_ARUCO_KEYS)+1)
arucoDict3X3 = createArucoDict(span, 3)
## [saveAruco(key, arucoDict3X3) for key in span]
#filter = np.array([[-1, -1, -1], [-1, 50, -1], [-1, -1, -1]])
#sharpen_img_1=cv2.filter2D(img,-1,filter)
bbox, ids = detectAruco(img, arucoDict3X3, blacklist=[0])
resultImg = drawAruco(img, bbox, ids)
showImage(resultImg)


'''
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    bbox, ids = detectAruco(img, arucoDict3X3, blacklist=None)
    print(ids)
    resultImg = drawAruco(img, bbox, ids)
    cv2.imshow('Image2', resultImg)
    if cv2.waitKey(1) == 27: break'''