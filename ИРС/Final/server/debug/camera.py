import socket
import cv2
import math
import time

class Camera:
    def __init__(self, index, matrix, distortion):
        self.index = index
        self.matrix = matrix
        self.distortion = distortion

    def readRaw(self):
        rawImg = cv2.imread('../../distortion/dataset/mappp1/5.png') if self.index == 0 \
             else cv2.imread('../../distortion/dataset/mappp2/5.png')
        return rawImg

    def read(self):
        rawImg = self.readRaw()
        cameraImg = getUndistortedImage(rawImg, self.matrix, self.distortion)
        return cameraImg

def getUndistortedImage(img, mtx, dist):
    h, w = img.shape[:2]
    newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    dst = cv2.undistort(img, mtx, dist, None, newCameraMtx)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    return dst