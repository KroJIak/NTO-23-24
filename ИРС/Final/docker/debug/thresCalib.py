from cv2 import createTrackbar, getTrackbarPos
import cv2
from camera import Camera, showImage
import numpy as np

def nothing(*arg): pass

def createBars():
    cv2.namedWindow('buttons')
    createTrackbar('blockSize', 'buttons', 3, 255, nothing)
    createTrackbar('C', 'buttons', 0, 255, nothing)
    createTrackbar('sizeBlur', 'buttons', 1, 15, nothing)

def getBars():
    blockSize = getTrackbarPos('blockSize', 'buttons')
    C = getTrackbarPos('C', 'buttons')
    sizeBlur = getTrackbarPos('sizeBlur', 'buttons')
    blockSize = max(3, blockSize // 2 * 2 + 1)
    sizeBlur = max(1, sizeBlur)
    return blockSize, C, sizeBlur

def getBinaryImage(img, blockSize, C, sizeBlur):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBinary = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, C)
    imgBinary = cv2.blur(imgBinary, (sizeBlur, sizeBlur))
    return imgBinary

def main():
    camera = Camera(2)
    camera.setArucoSettings()
    createBars()
    while True:
        img = camera.read()
        blockSize, C, sizeBlur = getBars()
        imgBinary = getBinaryImage(img, blockSize, C, sizeBlur)
        imgCross = cv2.bitwise_and(img, img, mask=imgBinary)
        imgBinary = cv2.cvtColor(imgBinary, cv2.COLOR_GRAY2BGR)
        imgShow = np.concatenate((img, imgBinary, imgCross), axis=1)
        cv2.imshow('Calib', imgShow)
        if cv2.waitKey(1) == 27: break
    img = camera.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    showImage(imgGray)
    print(f'blockSize={blockSize}, C={C}, sizeBlur={sizeBlur}')
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()