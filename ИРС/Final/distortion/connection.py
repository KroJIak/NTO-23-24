from server.solution.const import ConstPlenty
from server.solution.vision import getUndistortedImage, getFullScene
import cv2
import os

class Camera:
    def __init__(self, url, matrix, distortion):
        self.cap = cv2.VideoCapture(url)
        self.matrix = matrix
        self.distortion = distortion

    def readRaw(self):
        success, rawImg = self.cap.read()
        return rawImg if success else None

    def read(self):
        rawImg = self.readRaw()
        cameraImg = getUndistortedImage(rawImg, self.matrix, self.distortion)
        return cameraImg

def makeNewPhoto(resImg):
    path = 'conns'
    fileNum1 = len(os.listdir(f'{path}/'))
    cv2.imwrite(f'{path}/{fileNum1}.png', resImg)

const = ConstPlenty()
cam1 = Camera('http://student:nto2024@10.128.73.31/mjpg/video.mjpg', const.cam1.matrix, const.cam1.distortion)
cam2 = Camera('http://student:nto2024@10.128.73.38/mjpg/video.mjpg', const.cam2.matrix, const.cam2.distortion)

while True:
    img1 = cam1.read()
    img2 = cam2.read()
    resImg = getFullScene(img1, img2)
    cv2.imshow('Image', resImg)
    match cv2.waitKey(1):
        case 27: break
        case 32: makeNewPhoto(resImg)