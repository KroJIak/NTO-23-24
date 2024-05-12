import numpy as np
from cv2 import createTrackbar, getTrackbarPos
import cv2

def nothing(*arg): pass

def createBars(num):
    cv2.namedWindow(f'buttons-{num}')
    createTrackbar('hmin', f'buttons-{num}', 0, 255, nothing)
    createTrackbar('smin', f'buttons-{num}', 0, 255, nothing)
    createTrackbar('vmin', f'buttons-{num}', 0, 255, nothing)
    createTrackbar('hmax', f'buttons-{num}', 0, 255, nothing)
    createTrackbar('smax', f'buttons-{num}', 0, 255, nothing)
    createTrackbar('vmax', f'buttons-{num}', 0, 255, nothing)

def getBars(num):
    hmin = getTrackbarPos('hmin', f'buttons-{num}')
    smin = getTrackbarPos('smin', f'buttons-{num}')
    vmin = getTrackbarPos('vmin', f'buttons-{num}')
    hmax = getTrackbarPos('hmax', f'buttons-{num}')
    smax = getTrackbarPos('smax', f'buttons-{num}')
    vmax = getTrackbarPos('vmax', f'buttons-{num}')
    return hmin, smin, vmin, hmax, smax, vmax

def getBinaryImage(img, blockSize, C, sizeBlur):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBinary = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, C)
    imgBinary = cv2.blur(imgBinary, (sizeBlur, sizeBlur))
    return imgBinary

def main():
    countDiv = int(input('Введите количество делений: '))
    cap = cv2.VideoCapture(3)
    for n in range(countDiv): createBars(n)
    while True:
        _, img = cap.read()
        # img = cv2.imread('gewrgdfsger.png')
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        step = round(imgHSV.shape[0] / countDiv)
        imgBinaryArr = []
        for n in range(countDiv):
            hmin, smin, vmin, hmax, smax, vmax = getBars(n)
            imgHSVPart = imgHSV[step*n:step*(n+1)]
            imgBinaryPart = cv2.inRange(imgHSVPart, (hmin, smin, vmin), (hmax, smax, vmax))
            imgBinaryArr.append(imgBinaryPart)
        imgBinary = np.concatenate(imgBinaryArr, axis=0)
        imgCross = cv2.bitwise_and(img, img, mask=imgBinary)
        imgBinary = cv2.cvtColor(imgBinary, cv2.COLOR_GRAY2BGR)
        imgShow = np.concatenate((img, imgBinary, imgCross), axis=1)
        cv2.imshow('Calib', imgShow)
        if cv2.waitKey(1) == 27: break
    if countDiv == 1:
        hmin, smin, vmin, hmax, smax, vmax = getBars(0)
        print(f"imgBinary = cv2.inRange(imgHSV, ({hmin}, {smin}, {vmin}), ({hmax}, {smax}, {vmax}))")
    else:
        for n in range(countDiv):
            hmin, smin, vmin, hmax, smax, vmax = getBars(n)
            print(f"imgBinary{n+1} = cv2.inRange(imgHSV[{step*n}:{step*(n+1)}], ({hmin}, {smin}, {vmin}), ({hmax}, {smax}, {vmax}))")
        print(f"imgBinary = np.concatenate((" + ", ".join([f'imgBinary{n+1}' for n in range(countDiv)]) +"), axis=0)")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()