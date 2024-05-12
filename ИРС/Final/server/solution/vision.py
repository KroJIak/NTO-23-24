import traceback

import cv2
import numpy as np
import math
from functools import lru_cache

def getUndistortedImage(img, mtx, dist):
    h, w = img.shape[:2]
    newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    dst = cv2.undistort(img, mtx, dist, None, newCameraMtx)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    return dst

def getStitcheredImage(img1, img2, mode=cv2.STITCHER_PANORAMA):
    # img1 = cv2.rotate(img1, cv2.ROTATE_90_CLOCKWISE)
    # img2 = cv2.rotate(img2, cv2.ROTATE_90_CLOCKWISE)
    stitcher = cv2.Stitcher().create(mode)
    status, pano = stitcher.stitch([img1, img2])
    pano = cv2.rotate(pano, cv2.ROTATE_90_CLOCKWISE)
    return pano

def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def rotateImageByPoint(img, rotationPoint, theta, width, height):
    shape = (img.shape[1], img.shape[0])
    matrix = cv2.getRotationMatrix2D(center=rotationPoint, angle=math.degrees(theta), scale=1)
    resultImg = cv2.warpAffine(src=img, M=matrix, dsize=shape)
    x = int(rotationPoint[0] - width / 2)
    y = int(rotationPoint[1] - height / 2)
    resultImg = resultImg[y:y + height, x:x + width]
    return resultImg

def getFullScene(leftImg, rightImg):
    k = 0.8035
    rightImg = cv2.resize(rightImg, (int(rightImg.shape[1] * k), int(rightImg.shape[0] * k)))
    offsetCenter = -40
    leftImg = leftImg[68 + offsetCenter:]
    rightImg = rightImg[:-150 + offsetCenter, 9:861]
    resImg = np.concatenate((rightImg, leftImg), axis=0)
    resImg = rotateImage(resImg, 1.2)
    resImg = resImg[37:-37, 208:-93]
    resImg = cv2.rotate(resImg, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return resImg

def findContourCenter(cnt):
    cx, cy = None, None
    moment = cv2.moments(cnt)
    if moment['m00'] != 0:
        cx = int(moment['m10'] / moment['m00'])
        cy = int(moment['m01'] / moment['m00'])
    return (cx, cy)

def adaptiveThresholdImage(imgGray, blockSize, C):
    imgBinary = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, C)
    kernel = np.ones((9, 9), np.uint8)
    imgBinary = cv2.morphologyEx(imgBinary, cv2.MORPH_CLOSE, kernel)
    return imgBinary

def getRoadMask(img, show=False):
    #HSVMin = (93, 0, 50)
    #HSVMax = (134, 120, 164)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #imgBinary1 = cv2.inRange(imgHSV[:imgHSV.shape[0]*2//3], (98, 32, 74), (130, 107, 163))
    #imgBinary2 = cv2.inRange(imgHSV[imgHSV.shape[0]*2//3:], (83, 25, 56), (136, 123, 113))
    imgBinary1 = cv2.inRange(imgHSV[0:276], (63, 31, 68), (133, 161, 183))
    imgBinary2 = cv2.inRange(imgHSV[276:552], (73, 26, 51), (152, 201, 149))
    imgBinary = np.concatenate((imgBinary1, imgBinary2), axis=0)
    if show: showImage(imgBinary)
    kernel = np.ones((9, 9), np.uint8)
    imgBinary = cv2.morphologyEx(imgBinary, cv2.MORPH_OPEN, kernel)
    if show: showImage(imgBinary)
    kernel = np.ones((17, 17), np.uint8)
    imgBinary = cv2.morphologyEx(imgBinary, cv2.MORPH_CLOSE, kernel)
    if show: showImage(imgBinary)
    kernel = np.ones((9, 9), np.uint8)
    imgBinary = cv2.erode(imgBinary, kernel, iterations=4)
    if show: showImage(imgBinary)
    return imgBinary

def getGreenMask(img, show=False):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgBinary = cv2.inRange(imgHSV, (68, 53, 170), (90, 89, 255))
    if show: showImage(imgBinary)
    kernel = np.ones((12, 12), np.uint8)
    imgBinary = cv2.morphologyEx(imgBinary, cv2.MORPH_CLOSE, kernel)
    if show: showImage(imgBinary)
    kernel = np.ones((4, 9), np.uint8)
    imgBinary = cv2.dilate(imgBinary, kernel, iterations=4)
    if show: showImage(imgBinary)
    return imgBinary

def markupThresholdImage(img, show=False):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imgBinary1 = cv2.threshold(imgGray[:100], 160, 255, cv2.THRESH_BINARY)
    _, imgBinary2 = cv2.threshold(imgGray[100:200], 150, 255, cv2.THRESH_BINARY)
    _, imgBinary3 = cv2.threshold(imgGray[200:300], 150, 255, cv2.THRESH_BINARY)
    _, imgBinary4 = cv2.threshold(imgGray[300:400], 115, 255, cv2.THRESH_BINARY)
    _, imgBinary5 = cv2.threshold(imgGray[400:], 80, 255, cv2.THRESH_BINARY)
    if show:
        showImage(imgBinary1)
        showImage(imgBinary2)
        showImage(imgBinary3)
        showImage(imgBinary4)
        showImage(imgBinary5)
    imgBinary = np.concatenate((imgBinary1, imgBinary2, imgBinary3, imgBinary4, imgBinary5), axis=0)
    if show: showImage(imgBinary)
    kernel = np.ones((2, 2), np.uint8)
    imgBinary = cv2.dilate(imgBinary, kernel, iterations=2)
    if show: showImage(imgBinary)
    imgRoadMask = getRoadMask(img, show=show)
    imgGreenMask = getGreenMask(img, show=show)
    imgBinary = cv2.bitwise_and(imgBinary, imgBinary, mask=imgRoadMask)
    if show: showImage(imgBinary)
    resultImgBinary = cv2.bitwise_and(imgBinary, imgBinary, mask=cv2.bitwise_not(imgGreenMask))
    if show: showImage(resultImgBinary)
    return resultImgBinary

def getMarkupPositions(img, squareRange=(10, 115), adaptive=False, custom=True, show=False):
    if adaptive: imgBinary = adaptiveThresholdImage(img, 151, 1)
    elif custom:
        imgBinary = markupThresholdImage(img, show=True)
        imgBinary[:, -16:] = 0
        showImage(imgBinary)
    else:  _, imgBinary = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY)
    if show: showImage(imgBinary)
    contours, _ = cv2.findContours(imgBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    markupContours = [cnt for cnt in contours if squareRange[0] < cv2.contourArea(cnt) < squareRange[1]]
    markupArray = [findContourCenter(cnt) for cnt in markupContours]
    if show:
        imgContours = img.copy()
        cv2.drawContours(imgContours, markupContours, -1, (255, 0, 0), 1)
        [cv2.putText(imgContours, str(i), (center[0] - 4, center[1] - 4), cv2.FONT_HERSHEY_COMPLEX, 0.3, (100, 0, 255),0)
         for i, center in enumerate(markupArray)]
        showImage(imgContours)
    return markupArray

@lru_cache(None)
def getDistanceBetweenPoints(point1, point2):
    return math.hypot(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))


def minDistanceBetweenLines(line1, line2):
    return min([getDistanceBetweenPoints(point1, point2) for point1 in line1 for point2 in line2])

def getPointOnSameLineOnSquare(vertexes, minDist, maxDist):
    limitDist = minDist + (minDist + maxDist) // 2
    for i, pos1 in enumerate(vertexes[:-1]):
        for j, pos2 in enumerate(vertexes[i + 1:]):
            if math.hypot(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1])) < limitDist:
                return pos1, pos2

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

def getNearestPoints(points):
    distances = []
    for i, pnt1 in enumerate(points):
        for j, pnt2 in enumerate(points[i+1:], start=i+1):
            distances.append((getDistanceBetweenPoints(pnt1, pnt2), pnt1, pnt2))
    nearestPoints = sorted(distances, key=lambda x: x[0])[0][1:]
    return nearestPoints


def binaryCenterRobotImage(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgBinary = cv2.inRange(imgHSV[0:276], (106, 126, 164), (137, 166, 215))
    return imgBinary

def binaryOrientationPointsImage(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgBinary = cv2.inRange(imgHSV[0:551], (79, 99, 146), (177, 154, 238))
    return imgBinary

def getRobotCenterContour(imgBinary):
    contours, _ = cv2.findContours(imgBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if not contours: return None
    centerRobot = findContourCenter(contours[0])
    return centerRobot

def getOrientationPointsContour(imgBinary):
    contours, _ = cv2.findContours(imgBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if not contours: return None
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    orientationPoints = [findContourCenter(cnt) for cnt in contours]
    orientationPoints = orientationPoints[:4]
    return orientationPoints

def getRobotPoints(img, show=False):
    imgBinaryCenter = binaryCenterRobotImage(img)
    imgBinaryOrientation = binaryOrientationPointsImage(img)
    imgBinaryOrientation = cv2.bitwise_and(imgBinaryOrientation, imgBinaryOrientation, mask=cv2.bitwise_not(imgBinaryCenter))
    if show:
        showImage(imgBinaryCenter)
        showImage(imgBinaryOrientation)
    centerRobot = getRobotCenterContour(imgBinaryCenter)
    orientationPoints = getOrientationPointsContour(imgBinaryOrientation)
    return centerRobot, orientationPoints

def detectRobot(img, show=False):
    centerRobot, orientationPoints = getRobotPoints(img, show=False)
    if not centerRobot or not orientationPoints: return None
    nearestPoints = getNearestPoints(orientationPoints)
    directionPoint = ((nearestPoints[0][0] + nearestPoints[1][0]) // 2,
                      (nearestPoints[0][1] + nearestPoints[1][1]) // 2)
    if False:
        imgShow = img.copy()
        cv2.circle(imgShow, centerRobot, 3, (0, 0, 255), -1)
        [cv2.circle(imgShow, pnt, 3, (255, 255, 255), -1) for pnt in orientationPoints]
        showImage(imgShow)
    return centerRobot, directionPoint
def findPoints(img1, img2, img):
    pass

def showImage(img):
    while cv2.waitKey(1) != 27: cv2.imshow('Image', img)