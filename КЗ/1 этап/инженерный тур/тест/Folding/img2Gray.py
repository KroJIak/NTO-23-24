import cv2
import numpy as np

def convertImg2GrayByLightnessMethod(img):
    height, width = img.shape[:2]
    imgGray = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            color = list(img[i][j])
            grayShade = (min(color) + max(color)) / 2
            imgGray[i][j] = int(grayShade)
    return imgGray

def convertImg2GrayByAverageMethod(img):
    height, width = img.shape[:2]
    imgGray = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            color = list(img[i][j])
            grayShade = sum(color) / 3
            imgGray[i][j] = int(grayShade)
    return imgGray

def convertImg2GrayByLuminosityMethod(img):
    height, width = img.shape[:2]
    imgGray = np.zeros((height, width), dtype=np.uint8)
    kR, kG, kB = 0.3, 0.59, 0.11
    for i in range(height):
        for j in range(width):
            R, G, B = img[i][j]
            grayShade = R*kR + G*kG + B*kB
            imgGray[i][j] = int(grayShade)
    return imgGray

def convertImg2GrayByCV2Method(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return imgGray

def main():
    img = cv2.imread('image.png')
    imgGray1 = convertImg2GrayByLightnessMethod(img)
    imgGray2 = convertImg2GrayByAverageMethod(img)
    imgGray3 = convertImg2GrayByLuminosityMethod(img)
    imgGray4 = convertImg2GrayByCV2Method(img)
    while cv2.waitKey(1) != 27:
        cv2.imshow('RGB', img)
        cv2.imshow('Gray1', imgGray1)
        cv2.imshow('Gray2', imgGray2)
        cv2.imshow('Gray3', imgGray3)
        cv2.imshow('Gray4', imgGray4)

if __name__ == '__main__':
    main()