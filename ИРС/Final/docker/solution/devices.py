import socket
import cv2
import math
import time

class Robot:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.stop()
        self.resetRegulator()

    def send(self, message):
        self.sock.sendto(message, (self.ip, self.port))

    def resetRegulator(self):
        self.oldError = 0

    def angleRegulator(self, error, maxSpeed, angleLimit=8, kp=5, kd=10):
        if abs(error) < math.radians(angleLimit): speed = maxSpeed
        else: speed = 0
        u = error * kp + (error - self.oldError) * kd
        self.oldError = error
        self.turnRight(speed + u)
        self.turnLeft(speed - u)

    def rotate360(self, speedR=60, speedL=-55, timer=2.65):
        lastTime = time.time()
        self.turnRight(speedR)
        self.turnLeft(speedL)
        while lastTime + timer > time.time(): pass
        self.stop()

    def turnRight(self, speed):
        command = f'0:{speed}'
        self.send(command.encode('utf-8'))

    def turnLeft(self, speed):
        command = f'1:{speed}'
        self.send(command.encode('utf-8'))

    def stop(self):
        for dir in range(2):
            command = f'{dir}:0'
            self.send(command.encode('utf-8'))

    def bstop(self):
        for dir in range(2):
            command = f'{dir}:1'
            self.send(command.encode('utf-8'))

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