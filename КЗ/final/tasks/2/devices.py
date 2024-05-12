import numpy as np
import cv2

# класс для удобного работы с камерой
class Camera:
    def __init__(self, index: int, systemIsWindows: bool):
        self.index = index
        self.realCornerPoints = ()
        self.virtualCornerPoints = ()
        if systemIsWindows: self.cap = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
        else: self.cap = cv2.VideoCapture(self.index)
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 1)
        self.cap.set(cv2.CAP_PROP_EXPOSURE, 45)

    # получить обычное изображение с камеры
    def readRaw(self):
        success, img = self.cap.read()
        return img if success else None

    # получить исправленное изображение с камеры
    def read(self):
        rawImg = self.readRaw()
        resultImg = self.transformPerspective(rawImg)
        return resultImg

    # выставить углы изображения проекции проектора
    def setCornerPoints(self, realCornerPoints: tuple, virtualCornerPoints: tuple):
        self.realCornerPoints = np.float32(realCornerPoints)
        self.virtualCornerPoints = np.float32(virtualCornerPoints)

    # изменить изображение в соответствии с перспективой
    def transformPerspective(self, img):
        if not len(self.realCornerPoints) or not len(self.virtualCornerPoints):
            raise ValueError('The camera is not setup')
        transformMatrix = cv2.getPerspectiveTransform(self.realCornerPoints, self.virtualCornerPoints)
        resultImg = cv2.warpPerspective(img, transformMatrix, (img.shape[1], img.shape[0]))
        return resultImg