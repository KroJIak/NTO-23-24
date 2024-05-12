from modules.utils import getSampleData
import numpy as np
import base64
import cv2
import os

def showImage(img, winName='Image'):
    while cv2.waitKey(1) != 27: cv2.imshow(winName, img)

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
# if nameImgFile not in os.listdir('maps'): cv2.imwrite(nameImgFile, img)

showImage(img)