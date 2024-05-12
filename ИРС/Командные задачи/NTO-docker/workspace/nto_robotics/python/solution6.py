import sys
import os
import time

from nto_sim.py_nto_task6 import Task
import cv2

## Здесь должно работать ваше решение
def solve(task: Task):
    import numpy as np
    from math import radians
    ROBOT_NUM = 0
    VOLTAGES = [0, 0]
    class Motor():
        def __init__(self, robotNum, port):
            self.robotNum = robotNum
            self.port = port
            self.maxVoltage = 25
        def setSpeed(self, percent):
            VOLTAGES[self.port] = (max(0, min(100, percent)) * self.maxVoltage) / 100
            task.setMotorVoltage(self.robotNum, VOLTAGES)
        def getAngle(self, state):
            if self.port == 0: return radians(state.leftMotorAngle)
            elif self.port == 1: return radians(state.rightMotorAngle)
        def getAngularSpeed(self, state):
            if self.port == 0: return state.leftMotorSpeed
            elif self.port == 1: return state.rightMotorSpeed

    ## Загружаем изображение из задачи
    ## сцена отправляется с определенной частотй
    ## для этого смотри в документацию к задаче
    # mapImage = task.getTaskMap()
    # cv2.imwrite('../data/ex1-map.png', mapImage)
    # countRobots = task.robotsSize()
    # print('Number of robots:', countRobots)
    # state = task.getRobotState(ROBOT_NUM)
    # print("Left Motor angle:", state.leftMotorAngle)
    # print("Right Motor angle:", state.rightMotorAngle)
    # print("Left Motor speed:", state.leftMotorSpeed)
    # print("Right Motor speed:", state.rightMotorSpeed)

    taskInfo = task.getTask()
    print('Task: ', taskInfo)

    M1 = Motor(ROBOT_NUM, 0)
    M2 = Motor(ROBOT_NUM, 1)

    sceneImg = task.getTaskScene()
    SIZE = np.array((sceneImg.shape[1]/1.2, sceneImg.shape[0]/1.2), dtype=int)

    while True:
        state = task.getRobotState(ROBOT_NUM)
        sceneImg = task.getTaskScene()

        M1.setSpeed(0)
        M2.setSpeed(50)
        print(M1.getAngle(state), M2.getAngle(state))

        cv2.imshow('Scene', cv2.resize(sceneImg, SIZE))
        key = cv2.waitKey(int(1000/30)) # мс
        if key == 27: return
        # time.sleep(1/30)

if __name__ == '__main__':
    ## Запуск задания и таймера (внутри задания)
    task = Task()
    task.start()

    try:
        solve(task)
    except Exception as e:
        print(e)

    task.stop()
