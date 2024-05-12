import cv2
import numpy as np
import os

# PATH = os.getcwd()
# os.chdir(f'{PATH}/Folding')

kernelGaussian = np.array([
    [0.000789, 0.006581, 0.013347, 0.006581, 0.000789],
    [0.054901, 0.054901, 0.111345, 0.013347, 0.111345],
    [0.225821, 0.111345, 0.013347, 0.006581, 0.006581],
    [0.054901, 0.111345, 0.054901, 0.006581, 0.000789],
    [0.006581, 0.013347, 0.0065811, 0.006581, 0.000789]
])

kernelHorizontalSobel = np.array([
    [1, 0, -1],
    [2, 0, -2],
    [1, 0, -1]
])

def foldingImg2FeatureMap(imgGray, kernel):
    height, width = imgGray.shape[:2]
    imgFeatureMap = np.zeros((height, width), dtype=np.uint8)
    divNormal = 1 / 23
    for i in range(1, height-2):
        for j in range(1, width-2):
            resultArr, was = [], set()
            for g in range(-1, 2):
                for h in range(-1, 2):
                    if (g, h) not in was:
                        valueCell = imgGray[i+g][j+h] * kernel[g+1][h+1]
                        resultArr.append(valueCell)
                        was.add((g, h))
            grayShade = sum(resultArr)
            imgFeatureMap[i-1][j-1] = grayShade * divNormal
    return imgFeatureMap

def foldingImg2FeatureMapByCVMethod(imgGray, kernel):
    imgFeatureMap = cv2.filter2D(imgGray, -1, kernel)
    return imgFeatureMap

def main():
    img = cv2.imread('image.png')
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    imgFeatureMap1 = foldingImg2FeatureMap(imgGray, kernelHorizontalSobel)
    imgFeatureMap2 = foldingImg2FeatureMapByCVMethod(imgGray, kernelHorizontalSobel)
    while cv2.waitKey(1) != 27:
        cv2.imshow('RGB', img)
        cv2.imshow('Gray', imgGray)
        cv2.imshow('FeatureMap1', imgFeatureMap1)
        cv2.imshow('FeatureMap2', imgFeatureMap2)

if __name__ == '__main__':
    main()