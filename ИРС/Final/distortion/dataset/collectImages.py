import cv2
import os

def makeNewPhoto(img1, img2):
    folder = 'mappp'
    fileNum1 = len(os.listdir(f'{folder}1/'))
    fileNum2 = len(os.listdir(f'{folder}2/'))
    cv2.imwrite(f'{folder}1/{fileNum1}.png', img1)
    cv2.imwrite(f'{folder}2/{fileNum2}.png', img2)

cam1 = cv2.VideoCapture('http://student:nto2024@10.128.73.31/mjpg/video.mjpg')
cam2 = cv2.VideoCapture('http://student:nto2024@10.128.73.38/mjpg/video.mjpg')

while True:
    success1, img1 = cam1.read()
    success2, img2 = cam2.read()
    if success1: cv2.imshow('Camera1', img1)
    if success2: cv2.imshow('Camera2', img2)
    match cv2.waitKey(1):
        case 27: break
        case 32: makeNewPhoto(img1, img2)

cam1.release()
cv2.destroyAllWindows()