import requests
from time import time as gtime, sleep

HOME_URL = 'http://192.168.1.1'
FORWARD = 1
RELEASE = 0
BACKWARD = -1

def checkStatusCode(statusCode):
    if statusCode != 200:
        raise ValueError(f'Ошибка при отправке запроса: {statusCode}')

class Motor():
    def __init__(self, number):
        self.motorURL = f'{HOME_URL}/motor/{number}'
        self.lastEncoder = 0

    def run(self, direction):
        endPoint = f'{self.motorURL}/run'
        response = requests.post(endPoint, str(direction))
        checkStatusCode(response.status_code)

    def setSpeed(self, speed):
        endPoint = f'{self.motorURL}/set-speed'
        response = requests.post(endPoint, str(speed))
        checkStatusCode(response.status_code)

    def getEncoder(self):
        endPoint = f'{self.motorURL}/get-encoder'
        response = requests.get(endPoint)
        checkStatusCode(response.status_code)
        encoder = int(response.text) - self.lastEncoder
        return encoder

    def resetEncoder(self):
        self.lastEncoder = self.getEncoder()

M1 = Motor(1)
M2 = Motor(2)

def stop():
    M1.run(RELEASE)
    M2.run(RELEASE)
    M1.setSpeed(0)
    M2.setSpeed(0)

def reset():
    M1.resetEncoder()
    M2.resetEncoder()

def forwardTime(speed, time):
    M1.run(FORWARD)
    M2.run(FORWARD)
    M1.setSpeed(speed)
    M2.setSpeed(speed)
    sleep(time)
    stop()

def forward(speed, dist):
    reset()
    M1.run(FORWARD)
    M2.run(FORWARD)
    M1.setSpeed(speed)
    M2.setSpeed(speed)
    while (M1.getEncoder() + M2.getEncoder()) < dist: pass
    stop()

def backwardTime(speed, time):
    M1.run(BACKWARD)
    M2.run(BACKWARD)
    M1.setSpeed(speed)
    M2.setSpeed(speed)
    sleep(time)
    stop()

def backward(speed, dist):
    reset()
    M1.run(BACKWARD)
    M2.run(BACKWARD)
    M1.setSpeed(speed)
    M2.setSpeed(speed)
    while (abs(M1.getEncoder()) + abs(M2.getEncoder())) < dist: pass
    stop()

def rightTime(speed, time):
    reset()
    M1.run(BACKWARD)
    M2.run(FORWARD)
    M1.setSpeed(speed)
    M2.setSpeed(speed)
    sleep(time)
    stop()

def right(speed, dist):
    reset()
    M1.run(BACKWARD)
    M2.run(FORWARD)
    M1.setSpeed(speed)
    M2.setSpeed(speed)
    while abs(M2.getEncoder()) < dist: pass
    stop()

def leftTime(speed, time):
    reset()
    M1.run(FORWARD)
    M2.run(BACKWARD)
    M1.setSpeed(speed)
    M2.setSpeed(speed)
    sleep(time)
    stop()

def left(speed, dist):
    reset()
    M1.run(FORWARD)
    M2.run(BACKWARD)
    M1.setSpeed(speed)
    M2.setSpeed(speed)
    while abs(M1.getEncoder()) < dist: pass
    stop()
