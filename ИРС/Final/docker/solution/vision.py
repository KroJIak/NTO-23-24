from funcs import getNearestPoints
import numpy as np
import cv2

def findContourCenter(cnt):
    cx, cy = None, None
    moment = cv2.moments(cnt)
    if moment['m00'] != 0:
        cx = int(moment['m10'] / moment['m00'])
        cy = int(moment['m01'] / moment['m00'])
    return (cx, cy)

def adaptiveThresholdImage(imgGray, blockSize, C, sizeBlur):
    imgBinary = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, C)
    imgBinary = cv2.blur(imgBinary, (sizeBlur, sizeBlur))
    return imgBinary

def binaryCenterRobotImage(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    '''HSVMin = (41, 99, 38)
    HSVMax = (157, 214, 84)  # - 170
    imgBinary1 = cv2.inRange(imgHSV[:170], HSVMin, HSVMax)

    HSVMin = (52, 89, 32)
    HSVMax = (147, 179, 79)  # 170 - 310
    imgBinary2 = cv2.inRange(imgHSV[170:310], HSVMin, HSVMax)

    HSVMin = (44, 107, 31)
    HSVMax = (151, 200, 100)  # 310 - 380
    imgBinary3 = cv2.inRange(imgHSV[310:380], HSVMin, HSVMax)

    HSVMin = (96, 156, 17)
    HSVMax = (145, 255, 38)  # 380 -
    imgBinary4 = cv2.inRange(imgHSV[380:], HSVMin, HSVMax)

    imgBinary = np.concatenate((imgBinary1, imgBinary2, imgBinary3, imgBinary4), axis=0)'''
    imgBinary1 = cv2.inRange(imgHSV[0:120], (49, 104, 142), (138, 193, 208))
    imgBinary2 = cv2.inRange(imgHSV[120:240], (48, 86, 141), (126, 195, 216))
    imgBinary3 = cv2.inRange(imgHSV[240:360], (4, 91, 100), (139, 236, 215))
    imgBinary4 = cv2.inRange(imgHSV[360:480], (18, 101, 51), (130, 179, 198))
    imgBinary = np.concatenate((imgBinary1, imgBinary2, imgBinary3, imgBinary4), axis=0)

    return imgBinary

def binaryOrientationPointsImage(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    '''HSVMin = (33, 38, 62)
    HSVMax = (202, 255, 228)  # - 170
    imgBinary1 = cv2.inRange(imgHSV[:170], HSVMin, HSVMax)

    HSVMin = (16, 31, 62)
    HSVMax = (228, 220, 173)  # 170 - 310
    imgBinary2 = cv2.inRange(imgHSV[170:310], HSVMin, HSVMax)

    HSVMin = (39, 34, 52)
    HSVMax = (185, 138, 110)  # 310 - 380
    imgBinary3 = cv2.inRange(imgHSV[310:380], HSVMin, HSVMax)

    HSVMin = (27, 52, 32)
    HSVMax = (190, 164, 94)  # 380 -
    imgBinary4 = cv2.inRange(imgHSV[380:], HSVMin, HSVMax)

    imgBinary = np.concatenate((imgBinary1, imgBinary2, imgBinary3, imgBinary4), axis=0)'''
    imgBinary1 = cv2.inRange(imgHSV[0:120], (19, 15, 144), (216, 150, 255))
    imgBinary2 = cv2.inRange(imgHSV[120:240], (29, 24, 159), (188, 164, 224))
    imgBinary3 = cv2.inRange(imgHSV[240:360], (38, 44, 135), (229, 232, 220))
    imgBinary4 = cv2.inRange(imgHSV[360:480], (27, 21, 156), (185, 178, 222))
    imgBinary = np.concatenate((imgBinary1, imgBinary2, imgBinary3, imgBinary4), axis=0)
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

def showImage(img, winName='Image'):
    while cv2.waitKey(1) != 27: cv2.imshow(winName, img)