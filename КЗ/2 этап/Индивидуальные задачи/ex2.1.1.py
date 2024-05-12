import cv2
from math import pi, sqrt

def findContourCenter(cnt):
    cx, cy = None, None
    moment = cv2.moments(cnt)
    if moment['m00'] != 0:
        cx = moment['m10'] / moment['m00']
        cy = moment['m01'] / moment['m00']
    return (cx, cy)

resArr = []
for numImage in range(100):
    img = cv2.imread(f'assets/images/img{numImage}.png')
    imgCrop = img[59:-53, 144:-127]
    imgGray = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY)
    _, imgBinary = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(imgBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    figuraContour = contours[0]
    figuraArea = cv2.contourArea(figuraContour)
    center = findContourCenter(figuraContour)
    center = (round(center[0] / 5.8), round(center[1] / 5.8))
    radius = round(sqrt(figuraArea / pi) / 5.8)
    resArr.append([center[1], center[0], radius])

    '''while cv2.waitKey(1) != 27:
        cv2.imshow('Image', img)
        cv2.imshow('Image2', imgCrop)'''
cv2.destroyAllWindows()

print(str(resArr)[1:-1])