import math
import time

import numpy as np
import cv2

from const import ConstPlenty
from objects import *
from funcs import *

const = ConstPlenty()

class Window:
    def __init__(self, backgroundImg: np.array, freq: int, nameWindow='SceneImage'):
        self.backgroundImg = backgroundImg
        self.height, self.width = backgroundImg.shape[:2]
        self.freq = freq
        self.nameWindow = nameWindow

        self.sceneImg = self.backgroundImg

        self.balls = []
        self.walls = []

        self.show()
        cv2.setMouseCallback(nameWindow, self.checkMouse)

    def show(self):
        resultImg = self.backgroundImg.copy()
        resultImg = self.drawWalls(resultImg)
        resultImg = self.drawBalls(resultImg)
        cv2.imshow(self.nameWindow, resultImg)
        self.checkKeys()

    def drawBalls(self, img: np.array) -> np.array:
        self.updateBalls(img)
        resultImg = img.copy()
        for ball in self.balls:
            imgPos = (int(ball.pos.x), int(ball.pos.y))
            cv2.circle(resultImg, imgPos, ball.radius, ball.color, thickness=-1)
        return resultImg

    def drawWalls(self, img: np.array) -> np.array:
        resultImg = img.copy()
        for wall in self.walls:
            imgStartPos = (int(wall.startPos.x), int(wall.startPos.y))
            imgEndPos = (int(wall.endPos.x), int(wall.endPos.y))
            cv2.line(resultImg, imgStartPos, imgEndPos, wall.color, wall.thickness)
        return resultImg

    def updateBalls(self, img: np.array):
        for ball in self.balls:
            pointsOfNormal = []
            for angle in range(0, 360):
                radAngle = math.radians(angle)
                dx, dy = math.cos(radAngle) * ball.radius, math.sin(radAngle) * ball.radius
                imgShape = img.shape[:2]
                imgPos = (round(ball.pos.x+dx), round(ball.pos.y+dy))
                if 0 <= imgPos[1] < imgShape[0] and 0 <= imgPos[0] < imgShape[1]:
                    realColor = tuple(img[imgPos[1], imgPos[0]])
                    backgroundColor = tuple(self.backgroundImg[imgPos[1], imgPos[0]])
                    if realColor != backgroundColor: pointsOfNormal.append(Position(x=dx, y=dy))
            if pointsOfNormal:
                normal = getNormalByPoints(pointsOfNormal, ball.radius)
                direction = np.array([ball.velocity.x, ball.velocity.y])
                newVelocity = direction - normal * np.dot(normal, direction) * 2
                ball.velocity.x = newVelocity[0]
                ball.velocity.y = newVelocity[1]
            ball.pos.x += ball.velocity.x
            ball.pos.y += ball.velocity.y

    def checkKeys(self):
        key = cv2.waitKey(self.freq)
        match key:
            case 27: # Esc
                exit(0)

    def checkMouse(self, event, x, y, flags, param):
        mousePos = (x, y)
        match event:
            case cv2.EVENT_LBUTTONDOWN:
                pass

def main():
    # backgroundImg = cv2.imread('map.png')
    backgroundImg = np.zeros((1000, 1500, 3), dtype=np.uint8)
    backgroundImg[:, :, :] = 70
    window = Window(backgroundImg=backgroundImg, freq=const.DT)
    window.balls.append(Ball(Position(x=window.width//2, y=window.height//2), Velocity(1, 5), 50, const.color.yellow))
    window.walls.append(Wall(Position(x=-100, y=200), Position(x=100, y=200), const.wall.thickness, const.color.red))
    window.walls.append(Wall(Position(x=100, y=200), Position(x=200, y=0), const.wall.thickness, const.color.red))
    window.walls.append(Wall(Position(x=200, y=0), Position(x=100, y=-200), const.wall.thickness, const.color.red))
    window.walls.append(Wall(Position(x=100, y=-200), Position(x=-100, y=-200), const.wall.thickness, const.color.red))
    window.walls.append(Wall(Position(x=-100, y=-200), Position(x=-200, y=0), const.wall.thickness, const.color.red))
    window.walls.append(Wall(Position(x=-200, y=0), Position(x=-100, y=200), const.wall.thickness, const.color.red))
    for wall in window.walls:
        wall.startPos.x += window.width // 2
        wall.endPos.x += window.width // 2
        wall.startPos.y += window.height // 2
        wall.endPos.y += window.height // 2
    while True: window.show()


if __name__ == '__main__':
    main()