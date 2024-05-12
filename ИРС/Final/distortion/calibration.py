import os

import numpy as np
import cv2
from glob import glob

# размер шахматной доски
height, width = 8, 6
# размер одной клетки доски (в мм)
lenCell = 55

def getObjAndImgPoints(images, sizeBoard, lenCell, show=False):
    height, width = sizeBoard
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, lenCell, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objPoint = np.zeros((width * height, 3), np.float32)
    objPoint[:, :2] = np.mgrid[0:height, 0:width].T.reshape(-1, 2)
    # Arrays to store object points and image points from all the images.
    objectPoints = []  # 3d point in real world space
    imgPoints = []  # 2d points in image plane.
    for i, (file, img) in enumerate(images):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        try:
            ret, corners = cv2.findChessboardCorners(gray, (height, width), None)
            # If found, add object points, image points (after refining them)
            if ret: objectPoints.append(objPoint)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgPoints.append(corners2)
            if show:
                # Draw and display the corners
                cv2.drawChessboardCorners(img, (height, width), corners2, ret)
                kk = 1
                gimg = cv2.resize(img, (int(img.shape[1] * kk), int(img.shape[0] * kk)))
                #while cv2.waitKey(1) != 32: cv2.imshow('Image', gimg)
                cv2.destroyAllWindows()
        except: print(file)
    return objectPoints, imgPoints

def getCalibrationData(img, objectPoints, imgPoints):
    h, w = img.shape[:2]
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objectPoints, imgPoints, (w, h), None, None)
    return mtx, dist

def getUndistortedImage(img, mtx, dist):
    h, w = img.shape[:2]
    newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newCameraMtx)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    return dst

def main():
    folder = 'dataset/cam'
    calibImages = [(file, cv2.imread(f'{folder}/{file}')) for file in os.listdir(f'{folder}/')]
    print(len(calibImages))
    objectPoints, imgPoints = getObjAndImgPoints(calibImages, (height, width), lenCell, show=True)
    print(calibImages[0][1].shape)
    mtx, dist = getCalibrationData(calibImages[0][1], objectPoints, imgPoints)
    print(f'Mtx:\n{mtx}')
    print(f'Dist:\n{dist}')

    img = cv2.imread(f'{folder}/5.jpg')
    undistortedImage = getUndistortedImage(img, mtx, dist)
    cv2.imwrite('undistortedImage.jpg', undistortedImage)


if __name__ == '__main__':
    main()