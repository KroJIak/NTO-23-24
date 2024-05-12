import math
import time
import random

import numpy as np
import cv2
from screeninfo import get_monitors

from const import ConstPlenty
from calib import getCameraCornerPoints, getProjectorCornerPoints
from devices import *
from objects import *
from funcs import *

# CONST
const = ConstPlenty()
run = True
balloons = []
collisionFlag = True

class Offset:
    def __init__(self):
        self.leftUp = [0, 0]
        self.rightDown = [0, 0]

# класс игрового окна
class Window:
    def __init__(self, backgroundImg: np.array, freq: int, offsetBorder: int, coefInfoBar: int,
                 fullscreen: bool = False, nameWindow: str = 'SceneImage', nameBinaryWindow: str = 'BinarySceneImage'):
        self.backgroundImg = backgroundImg
        self.freq = freq
        self.offsetBorder = offsetBorder
        self.coefInfoBar = coefInfoBar
        self.fullscreen = fullscreen
        self.nameWindow = nameWindow
        self.nameBinaryWindow = nameBinaryWindow
        self.score = 0

        self.height, self.width = backgroundImg.shape[:2]
        self.offset = Offset()
        self.createBorderPoints()
        self.createBasketPoints()
        self.createBinaryBorders()
        self.clearImage()
        self.show()

        cv2.setMouseCallback(nameWindow, self.checkMouse)

    # вывод окна на экран пользователя
    def show(self):
        cv2.imshow(self.nameWindow, self.sceneImg)
        cv2.imshow(self.nameBinaryWindow, self.binaryImg)
        self.checkKeys()

    #Создает края окна
    def createBorderPoints(self):
        self.borderPoints = [Position(x=self.offsetBorder, y=self.offsetBorder * self.coefInfoBar),
                        Position(x=self.width - self.offsetBorder, y=self.offsetBorder * self.coefInfoBar),
                        Position(x=self.width - self.offsetBorder, y=self.height - self.offsetBorder),
                        Position(x=self.offsetBorder, y=self.height - self.offsetBorder), ]

    #Создание корзины
    def createBasketPoints(self):
        self.basketPoints = [Position(x=self.width - self.offsetBorder - 400, y=self.height - self.offsetBorder - 200),
                        Position(x=self.width - self.offsetBorder - 40, y=self.height - self.offsetBorder - 200),
                        Position(x=self.width - self.offsetBorder - 400, y=self.height - self.offsetBorder - 40),
                        Position(x=self.width - self.offsetBorder - 40, y=self.height - self.offsetBorder - 40)]

    # создание отскоков от краев экрана и от корзины
    def createBinaryBorders(self):
        self.binaryBorders = [BinaryBorder(self.borderPoints[0], self.borderPoints[1], const.binaryBorder.thickness, const.binaryBorder.color),
                              BinaryBorder(self.borderPoints[1], self.borderPoints[2], const.binaryBorder.thickness, const.binaryBorder.color),
                              BinaryBorder(self.borderPoints[2], self.borderPoints[3], const.binaryBorder.thickness, const.binaryBorder.color),
                              BinaryBorder(self.borderPoints[3], self.borderPoints[0], const.binaryBorder.thickness, const.binaryBorder.color),
                              BinaryBorder(self.basketPoints[1], self.basketPoints[3], const.basket.thickness, const.basket.color),
                              BinaryBorder(self.basketPoints[3], self.basketPoints[2], const.basket.thickness, const.basket.color),
                              BinaryBorder(self.basketPoints[2], self.basketPoints[0], const.basket.thickness, const.basket.color)]

    # Рисование краев в бинарном окне
    def drawBinaryBorders(self):
        for bdr in self.binaryBorders:
            cv2.line(self.sceneImg, (bdr.startPos.x, bdr.startPos.y), (bdr.endPos.x, bdr.endPos.y), bdr.color, bdr.thickness)
            cv2.line(self.binaryImg, (bdr.startPos.x, bdr.startPos.y), (bdr.endPos.x, bdr.endPos.y), 255, bdr.thickness)

    # нарисовать белые круги
    def drawBalloons(self) -> np.array:
        global balloons
        for bln in balloons:
            imgPos = (int(bln.pos.x), int(bln.pos.y))
            cv2.circle(self.sceneImg, imgPos, bln.radius, bln.color, thickness=-1)

    # очистить изображение от игровых элементов
    def clearImage(self):
        self.sceneImg = self.backgroundImg.copy()
        self.binaryImg = np.zeros((self.height, self.width, 1), dtype=np.uint8)

    # Вызывает функции для верхней панели
    def drawInfoBar(self):
        self.drawInstruction()
        self.drawScore()

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

    # Рисует инструкции в верху экрана
    def drawInstruction(self):
        cv2.putText(self.sceneImg, const.text.insturction, (60, 100),
                    cv2.FONT_HERSHEY_COMPLEX, self.width * (1 / 1700), (255, 255, 255), 2)
        cv2.putText(self.sceneImg, const.text.insturction_2, (self.width // 2 - 420, 170),
                    cv2.FONT_HERSHEY_COMPLEX, self.width * (1 / 1700), (255, 255, 255), 2)

    # Создает текст с очками
    def drawScore(self):
        cv2.putText(self.sceneImg, f'{const.text.score}: {self.score}', (50, 170),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    # Отрисовка меню победы
    def drawWinMenu(self):
        self.clearImage()
        cv2.putText(self.sceneImg, const.text.win, (self.width // 2 - 460, self.height // 2 + 10),
                    cv2.FONT_HERSHEY_COMPLEX, self.width * (1 / 2000), (255, 255, 255), 2)
        cv2.rectangle(self.sceneImg, (self.width // 2 - 480, self.height // 2 - 30),
                      (self.width // 2 + 480, self.height // 2 + 30), (255, 255, 255), 2)
        self.show()
        cv2.waitKey(0)

    def setFullscreen(self):
        self.fullscreen = not self.fullscreen
        cv2.destroyWindow(self.nameWindow)
        cv2.namedWindow(self.nameWindow, cv2.WND_PROP_FULLSCREEN)
        if self.fullscreen: cv2.setWindowProperty(self.nameWindow, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(self.nameWindow, self.sceneImg)

    # проверить нажатие клавиши
    def checkKeys(self):
        global run
        key = cv2.waitKey(self.freq)
        match key:
            case 27: # Esc
                run = False
            case 32: # Space
                self.setFullscreen()
            case 114: # R
                removeLastBalloon()
            case 1082: # К
                removeLastBalloon()


    # проверить нажатие мыши
    def checkMouse(self, event, x, y, flags, param):
        mousePos = (x, y)
        match event:
            case cv2.EVENT_LBUTTONDOWN:
                pass

# Создает коллизию для шаров
def addCollisionBalloons(balloon: Balloon, binaryImg: np.array):
    global collisionFlag
    pointsOfNormal = []
    balloonBinaryImg = np.zeros((binaryImg.shape[0], binaryImg.shape[1], 1), dtype=np.uint8)
    cv2.circle(balloonBinaryImg, (int(balloon.pos.x), int(balloon.pos.y)), balloon.radius + const.balloon.radiusOffset, 255, -1)
    sumSeparately = np.sum(balloonBinaryImg) + np.sum(binaryImg)
    sumTogether = np.sum(cv2.bitwise_or(balloonBinaryImg, binaryImg))
    collisionFlag = True
    if sumTogether != sumSeparately and collisionFlag:
        for angle in range(0, 360):
            radAngle = math.radians(angle)
            dx, dy = math.cos(radAngle) * (balloon.radius + const.balloon.radiusOffset), math.sin(radAngle) * (balloon.radius + const.balloon.radiusOffset)
            imgShape = binaryImg.shape[:2]
            imgPos = (int(balloon.pos.x + dx), int(balloon.pos.y + dy))
            if 0 <= imgPos[1] < imgShape[0] and 0 <= imgPos[0] < imgShape[1]:
                binaryValue = int(binaryImg[imgPos[1], imgPos[0]])
                if binaryValue: pointsOfNormal.append(Position(x=dx, y=dy))
        if pointsOfNormal:
            normal = getNormalByPoints(pointsOfNormal, (balloon.radius + const.balloon.radiusOffset))
            direction = np.array([balloon.velocity.x, balloon.velocity.y])
            newVelocity = direction - normal * np.dot(normal, direction) * 2
            balloon.velocity.x = newVelocity[0]
            balloon.velocity.y = newVelocity[1]
            collisionFlag = False
    else: collisionFlag = True

# обновить состояние кругов (их перемещение)
def updateBalloons(window: Window):
    global balloons
    removeBalloonsArr = []
    for bln in balloons:
        if not (window.offset.leftUp[0] <= bln.pos.x <= window.width - window.offset.rightDown[0] and window.offset.leftUp[1] <= bln.pos.y <= window.height - window.offset.rightDown[1]):
            removeBalloonsArr.append(bln)
            continue
        addCollisionBalloons(bln, window.binaryImg)
        bln.pos.x += bln.velocity.x
        bln.pos.y += bln.velocity.y
    for bln in removeBalloonsArr:
        balloons.remove(bln)

# Удаляет последний шар
def removeLastBalloon():
    global balloons
    if balloons: balloons.pop(-1)

# Проверка на нахождение мяча/мячей в корзине
def detectBalloonInBasket(window: Window):
    removeBalloonsArr = []
    for bln in balloons:
        balloonBinaryImg = np.zeros((window.height, window.width, 1), dtype=np.uint8)
        cv2.circle(balloonBinaryImg, (int(bln.pos.x), int(bln.pos.y)), bln.radius + const.balloon.radiusOffset, 255, -1)
        basketBinaryImg = np.zeros((window.height, window.width, 1), dtype=np.uint8)
        leftUpPoint, rightDownPoint = window.basketPoints[0], window.basketPoints[-1]
        cv2.rectangle(basketBinaryImg, (leftUpPoint.x, leftUpPoint.y), (rightDownPoint.x, rightDownPoint.y), 255, -1)
        sumBasket = np.sum(basketBinaryImg)
        sumTogether = np.sum(cv2.bitwise_or(balloonBinaryImg, basketBinaryImg))
        if sumBasket == sumTogether:
            removeBalloonsArr.append(bln)
    if len(removeBalloonsArr):
        window.drawWinMenu()
        for bln in removeBalloonsArr:
            balloons.remove(bln)
            window.score += 1

# Создание круга в случайном месте со случайной скоростью
def getNewBalloon(window: Window):
    newPosition = Position(x=window.width // 2, y=window.height // 2)
    randomSpeed = random.uniform(const.balloon.speedRange[0], const.balloon.speedRange[1])
    velocityX = random.uniform(-randomSpeed, randomSpeed)
    velocityY = random.uniform(randomSpeed + abs(velocityX), randomSpeed - abs(velocityX))
    newVelocity = Velocity(x=velocityX, y=velocityY)
    newBalloon = Balloon(newPosition, newVelocity, const.balloon.radius, const.color.white)
    return newBalloon

# Отрисовывает линии маркера в бинарном окне
def drawMarkerLines(img: np.array, window: Window):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgBinaryBlackLines = cv2.inRange(imgHSV, (0, 0, 0), (255, 255, 136))
    # imgBinaryRedLines = cv2.inRange(imgHSV, (0, 11, 0), (36, 255, 160))
    imgBinaryBlueLines = cv2.inRange(imgHSV, (0, 11, 31), (181, 207, 125))
    imgBinaryLines = cv2.bitwise_or(imgBinaryBlueLines, imgBinaryBlackLines)
    imgBinaryLines = cv2.resize(imgBinaryLines, (window.width, window.height))
    resultBinaryImg = cv2.bitwise_or(window.binaryImg, imgBinaryLines)
    resultBinaryImg = cv2.dilate(resultBinaryImg, None, iterations=2)
    window.binaryImg = resultBinaryImg

# Проверка на человека в кадре
def isHumanInImage(img: np.array):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgBinary = cv2.inRange(imgHSV, (54, 0, 134), (156, 76, 191))
    maxValue = (255 * img.shape[0] * img.shape[1])
    currentValue = np.sum(imgBinary)
    return maxValue // 2 > currentValue

# основная функция
def main(cameraIndex: int, systemIsWindows: bool):
    global balloons
    camera = Camera(cameraIndex, systemIsWindows)
    cameraCornerPoints = getCameraCornerPoints(camera)
    rawCameraImgShape = camera.readRaw().shape[:2]
    rawCameraImgShape = rawCameraImgShape[::-1]
    projectorCornerPoints = getProjectorCornerPoints(rawCameraImgShape)

    camera.setCornerPoints(cameraCornerPoints, projectorCornerPoints)
    const.screenBorder.leftUp, const.screenBorder.rightDown = cameraCornerPoints[0], cameraCornerPoints[-1]

    monitors = get_monitors()
    secondMonitor = monitors[1] if len(monitors) > 1 else monitors[0]
    userWindowSize = (secondMonitor.width, secondMonitor.height)
    backgroundImg = np.zeros((userWindowSize[1], userWindowSize[0], 3), dtype=np.uint8)
    window = Window(backgroundImg, const.DT, 50, 4)

    window.clearImage()
    window.drawStartButton()
    window.show()
    cv2.waitKey(0)

    lastPauseTime = time.time() + 15
    while run:
        if not balloons: balloons.append(getNewBalloon(window))
        cameraImg = camera.read()
        if isHumanInImage(cameraImg) and time.time() > lastPauseTime:

            window.show()
            continue
        window.clearImage()
        window.drawBinaryBorders()
        drawMarkerLines(cameraImg, window)
        updateBalloons(window)
        detectBalloonInBasket(window)
        window.drawInfoBar()
        window.drawBalloons()
        #cv2.imshow('Camera', cameraImg)
        window.show()


if __name__ == '__main__':
    print('[ Program started ]')
    cameraIndex = 1
    systemIsWindows = False
    main(cameraIndex, systemIsWindows)
    print('[ Program stopped ]')
