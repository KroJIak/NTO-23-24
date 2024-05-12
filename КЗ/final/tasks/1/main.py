import time
import random
from typing import List

import numpy as np
import cv2
from screeninfo import get_monitors

from const import ConstPlenty
from aruco import detectArucoMarkers
from calib import getCameraCornerPoints, getProjectorCornerPoints
from devices import *
from objects import *
from funcs import *

# CONST
const = ConstPlenty()
run = True

# класс смещения aruco метки
class Offset:
    def __init__(self):
        self.leftUp = [0, 0]
        self.rightDown = [0, 0]

# класс игрового окна
class Window:
    def __init__(self, backgroundImg: np.array, freq: int, fullscreen=False, nameWindow='SceneImage'):
        self.backgroundImg = backgroundImg
        self.freq = freq
        self.fullscreen = fullscreen
        self.nameWindow = nameWindow

        self.height, self.width = backgroundImg.shape[:2]
        self.setOffsetScale()
        self.offset = Offset()
        self.clearImage()
        self.show()

        self.timeOfLastBalloon = 0

        cv2.setMouseCallback(nameWindow, self.checkMouse)

    # вывод окна на экран пользователя
    def show(self):
        cv2.imshow(self.nameWindow, self.sceneImg)
        self.checkKeys()

    # выставить коэффициент увеличения экрана относительно реального размера проектора и виртуального окна
    def setOffsetScale(self):
        self.offsetScale = (self.width / (abs(const.border.rightDown[0] - const.border.leftUp[0])),
                            self.height / (abs(const.border.rightDown[1] - const.border.leftUp[1])))

    # нарисовать допустимую область
    def drawBorders(self, color: int):
        self.sceneImg[self.offset.leftUp[1]:-self.offset.rightDown[1],
                      self.offset.leftUp[0]:-self.offset.rightDown[0]] = color

    # нарисовать белые круги
    def drawBalloons(self, balloons: List[Balloon]) -> np.array:
        for bln in balloons:
            imgPos = (int(bln.pos.x), int(bln.pos.y))
            cv2.circle(self.sceneImg, imgPos, bln.radius, bln.color, thickness=-1)

    # очистить изображение от игровых элементов
    def clearImage(self):
        self.sceneImg = self.backgroundImg.copy()

    # обновить смещение по положениям Aruco маркеров
    def updateOffsetPosition(self, img: np.array):
        arucoDict = detectArucoMarkers(img)
        if const.arucoIds.leftUp in arucoDict:
            arucoLeftUpPos, borderLeftUpPos = arucoDict[const.arucoIds.leftUp], const.border.leftUp
            for axis in range(2):
                shift = arucoLeftUpPos[axis] - borderLeftUpPos[axis]
                shift = shift if shift > 0 else 0
                self.offset.leftUp[axis] = int(shift * self.offsetScale[axis])
        if const.arucoIds.rightDown in arucoDict:
            arucoRightDownPos, borderRightDownPos = arucoDict[const.arucoIds.rightDown], const.border.rightDown
            for axis in range(2):
                shift = borderRightDownPos[axis] - arucoRightDownPos[axis]
                shift = shift if shift > 0 else 1
                self.offset.rightDown[axis] = int(shift * self.offsetScale[axis])

    # вывести окно запуска
    def drawStartButton(self):
        cv2.putText(self.sceneImg, const.text.start, (self.width // 2 - 350, self.height // 2 + 10),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.rectangle(self.sceneImg, (self.width // 2 - 370, self.height // 2 - 30),
                      (self.width // 2 + 370, self.height // 2 + 30), (255, 255, 255), 2)
        cv2.putText(self.sceneImg, const.text.space, (self.width // 2 - 520, self.height // 2 - 200),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.rectangle(self.sceneImg, (self.width // 2 - 550, self.height // 2 - 270),
                      (self.width // 2 + 550, self.height // 2 - 150), (255, 255, 255), 2)
        self.show()

    # вывести окно перезапуска
    def drawRestartButton(self):
        cv2.putText(self.sceneImg, const.text.restart, (self.width // 2 -560, self.height // 2 + 10),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.rectangle(self.sceneImg, (self.width // 2 - 570, self.height // 2 - 30),
                      (self.width // 2 + 570, self.height // 2 + 30), (255, 255, 255), 2)
        self.show()

    def setFullscreen(self):
        self.fullscreen = not self.fullscreen
        cv2.namedWindow(self.nameWindow, cv2.WND_PROP_FULLSCREEN)
        if self.fullscreen: cv2.setWindowProperty(self.nameWindow, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # проверить нажатие клавиши
    def checkKeys(self):
        global run
        key = cv2.waitKey(self.freq)
        match key:
            case 27: # Esc
                run = False
            case 32: # Space
                self.setFullscreen()

    # проверить нажатие мыши
    def checkMouse(self, event, x, y, flags, param):
        mousePos = (x, y)
        match event:
            case cv2.EVENT_LBUTTONDOWN:
                pass

# обновить состояние кругов (их перемещение)
def updateBalloons(balloons: List[Balloon], window: Window):
    removeBalloonsArr = []
    for bln in balloons:
        if not (window.offset.leftUp[0] <= bln.pos.x <= window.width - window.offset.rightDown[0] and window.offset.leftUp[1] <= bln.pos.y <= window.height - window.offset.rightDown[1]):
            removeBalloonsArr.append(bln)
        if bln.pos.x <= window.offset.leftUp[0] + bln.radius or bln.pos.x >= window.width - window.offset.rightDown[0] - bln.radius:
            bln.velocity.x *= -1
        if bln.pos.y <= window.offset.leftUp[1] + bln.radius or bln.pos.y >= window.height - window.offset.rightDown[1] - bln.radius:
            bln.velocity.y *= -1
        bln.pos.x += bln.velocity.x
        bln.pos.y += bln.velocity.y
    for bln in removeBalloonsArr:
        balloons.remove(bln)

# Создание круга в случайном месте со случайной скоростью
def createBalloon(balloons: List[Balloon], window: Window):
    currentTime = time.time()
    if window.timeOfLastBalloon + const.balloon.createPeriod < currentTime:

        x_left = window.offset.leftUp[0] + const.balloon.radius + 10
        x_right = window.width - const.balloon.radius - 10 - window.offset.rightDown[0]
        y_up = const.balloon.radius + 10 + window.offset.leftUp[1]
        y_down = window.height - const.balloon.radius - 10 - window.offset.rightDown[1]
        if x_left > x_right or y_up > y_down: return

        position_x = random.randint(x_left, x_right)
        position_y = random.randint(y_up, y_down)
        newPosition = Position(x=position_x, y=position_y)

        randomSpeed = random.uniform(const.balloon.speedRange[0], const.balloon.speedRange[1])
        velocityX = random.uniform(-randomSpeed, randomSpeed)
        velocityY = random.uniform(randomSpeed + abs(velocityX), randomSpeed - abs(velocityX))
        newVelocity = Velocity(x=velocityX, y=velocityY)

        newBalloon = Balloon(newPosition, newVelocity, const.balloon.radius, const.color.white)
        balloons.append(newBalloon)
        window.timeOfLastBalloon = currentTime

def detectBallHit(img, window, balloons):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgHSV = imgHSV[const.border.leftUp[1]:const.border.rightDown[1],
             const.border.leftUp[0]:const.border.rightDown[0]]
    imgBinaryGreen = cv2.inRange(imgHSV, (40, 87, 84), (94, 255, 255))
    imgBinaryYellow = cv2.inRange(imgHSV, (0, 167, 113), (255, 255, 255))
    imgBinaryBlue = cv2.inRange(imgHSV, (83, 118, 33), (255, 255, 255))
    imgBinaryRed = cv2.inRange(imgHSV, (0, 162, 104), (13, 255, 255))
    hhhh = cv2.bitwise_or(imgBinaryBlue, cv2.bitwise_or(imgBinaryRed, cv2.bitwise_or(imgBinaryYellow, imgBinaryGreen)))
    cv2.imshow('Binary1', cv2.cvtColor(imgHSV, cv2.COLOR_HSV2BGR))
    cv2.imshow('Binary2', hhhh)
    for imgBinary in [imgBinaryGreen, imgBinaryBlue, imgBinaryYellow, imgBinaryRed]:
        imgBin = cv2.erode(imgBinary, None, iterations=2)
        imgBin = cv2.dilate(imgBin, None, iterations=2)
        contours, _ = cv2.findContours(imgBin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            maxContour = sorted(contours, key=lambda cnt: cv2.contourArea(cnt), reverse=True)[0]
            centerBall = findContourCenter(maxContour)
            windowPos = (int(centerBall[0] * window.offsetScale[0]), int(centerBall[1] * window.offsetScale[1]))
            removeBalloonsArr = []
            for bln in balloons:
                if distanceBetweenPositions(windowPos, (bln.pos.x, bln.pos.y)) < bln.radius * 2:
                    removeBalloonsArr.append(bln)
            for bln in removeBalloonsArr: balloons.remove(bln)
            cv2.circle(window.sceneImg, windowPos, 5, (0, 0, 255), -1)

# основная функция
def main(cameraIndex):
    camera = Camera(cameraIndex)
    cameraCornerPoints = getCameraCornerPoints(camera)
    rawCameraImgShape = camera.readRaw().shape[:2]
    rawCameraImgShape = rawCameraImgShape[::-1]
    projectorCornerPoints = getProjectorCornerPoints(rawCameraImgShape)

    camera.setCornerPoints(cameraCornerPoints, projectorCornerPoints, const.border.realArucoSize)
    const.border.leftUp, const.border.rightDown = cameraCornerPoints[0], cameraCornerPoints[-1]

    monitors = get_monitors()
    secondMonitor = monitors[1] if len(monitors) > 1 else monitors[0]
    userWindowSize = (secondMonitor.width, secondMonitor.height)
    backgroundImg = np.zeros((userWindowSize[1], userWindowSize[0], 3), dtype=np.uint8)
    window = Window(backgroundImg=backgroundImg, freq=const.DT)

    window.clearImage()
    window.drawStartButton()
    window.show()
    cv2.waitKey(0)

    balloons = []
    while run:
        updateBalloons(balloons, window)
        createBalloon(balloons, window)
        window.updateOffsetPosition(camera.readRaw())
        window.drawBorders(const.border.color)
        window.drawBalloons(balloons)
        cameraImg = camera.read()
        cv2.imshow('Camera', cameraImg)
        detectBallHit(cameraImg, window, balloons)
        window.show()
        window.clearImage()
        if len(balloons) > const.game.maxCountBalloons:
            balloons = []
            window.drawRestartButton()
            window.show()
            cv2.waitKey(0)

if __name__ == '__main__':
    print('[ Program started ]')
    cameraIndex = 3
    main(cameraIndex)
    print('[ Program stopped ]')
