import socket
import cv2
import math
import time
from vision import getUndistortedImage

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

    def angleRegulator(self, error, maxSpeed, angleLimit=8, kp=4, kd=10):
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
    def __init__(self, url, matrix, distortion):
        self.url = url
        self.matrix = matrix
        self.distortion = distortion
        self.cap = cv2.VideoCapture(url)

    def readRaw(self):
        success, readRaw = self.cap.read()
        return readRaw if success else None

    def read(self):
        rawImg = self.readRaw()
        cameraImg = getUndistortedImage(rawImg, self.matrix, self.distortion)
        return cameraImg