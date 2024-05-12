import numpy as np
import cv2

# класс для удобного работы с камерой
class Camera:
    def __init__(self, index: int):
        self.index = index
        self.realCornerPoints = ()
        self.virtualCornerPoints = ()
        self.cap = cv2.VideoCapture(self.index)

    def readRaw(self):
        success, img = self.cap.read()
        return img if success else None

    def read(self):
        rawImg = self.readRaw()
        resultImg = self.transformPerspective(rawImg)
        return resultImg

    def setCornerPoints(self, realCornerPoints: tuple, virtualCornerPoints: tuple, offset: int):
        self.realCornerPoints = np.float32(realCornerPoints)
        self.realCornerPoints[0] = (self.realCornerPoints[0][0] - offset, self.realCornerPoints[0][1] - offset)
        self.realCornerPoints[1] = (self.realCornerPoints[1][0] + offset, self.realCornerPoints[1][1] - offset)
        self.realCornerPoints[2] = (self.realCornerPoints[2][0] - offset, self.realCornerPoints[2][1] + offset)
        self.realCornerPoints[3] = (self.realCornerPoints[3][0] + offset, self.realCornerPoints[3][1] + offset)
        self.virtualCornerPoints = np.float32(virtualCornerPoints)


    def transformPerspective(self, img):
        if not len(self.realCornerPoints) or not len(self.virtualCornerPoints):
            raise ValueError('The camera is not setup')
        transformMatrix = cv2.getPerspectiveTransform(self.realCornerPoints, self.virtualCornerPoints)
        resultImg = cv2.warpPerspective(img, transformMatrix, (img.shape[1], img.shape[0]))
        return resultImg