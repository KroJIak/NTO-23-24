import cv2

class Camera:
    def __init__(self, index):
        self.cap = cv2.VideoCapture(index)
        self.setDefaultSettings()

    def setDefaultSettings(self):
        self.cap.set(3, 640)   # width
        self.cap.set(4, 480)   # height
        self.cap.set(10, 120)  # brightness
        self.cap.set(11, 50)   # contrast
        self.cap.set(12, 70)   # saturation
        self.cap.set(13, 13)   # hue
        self.cap.set(14, 50)   # gain
        self.cap.set(15, -3)        # exposure
        self.cap.set(17, 5000) # white_balance
        self.cap.set(28, 0)    # focus
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"PIM1"))

    def setArucoSettings(self):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 20)
        self.cap.set(cv2.CAP_PROP_SATURATION, 0)
        self.cap.set(cv2.CAP_PROP_FOCUS, 0)
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

    def read(self):
        success, img = self.cap.read()
        return img if success else None

    def release(self):
        self.setDefaultSettings()
        self.cap.release()

def showImage(img, winName='Image'):
    while cv2.waitKey(1) != 27: cv2.imshow(winName, img)

def main():
    cam = Camera(0)
    import time
    lastTime = time.time() + 5
    flag = True
    while True:
        if lastTime < time.time() and flag:
            cam.setArucoSettings()
            flag = False
        img = cam.read()
        cv2.imshow('Image', img)
        if cv2.waitKey(1) == 27: break
    cam.release()

if __name__ == '__main__':
    main()