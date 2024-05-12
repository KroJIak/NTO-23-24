import cv2
import numpy as np

def findContourCenter(cnt):
    cx, cy = None, None
    moment = cv2.moments(cnt)
    if moment['m00'] != 0:
        cx = int(moment['m10'] / moment['m00'])
        cy = int(moment['m01'] / moment['m00'])
    return (cx, cy)

cap = cv2.VideoCapture('assets/ex2.1.2.mp4')

resultArr = []
lastCenter = None
while True:
    success, img = cap.read()
    if not success: break

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imgBinary = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(imgBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    figuraContour = contours[2]
    center = findContourCenter(figuraContour)
    if lastCenter:
        moving = [center[i]-lastCenter[i] for i in range(1, -1, -1)]
        resMoving = [1 if mov > 0 else -1 if mov < 0 else 0 for i, mov in enumerate(moving)]
        resultArr.append((resMoving[0], resMoving[1]))
    lastCenter = center

    '''while cv2.waitKey(1) != 27:
        cv2.circle(img, center, 2, (255, 0, 0), 2)
        cv2.drawContours(img, [figuraContour], -1, (255, 0, 255), 1)
        cv2.imshow('Image', img)'''

cv2.destroyAllWindows()
cap.release()

print(str(resultArr)[1:-1])