import time
import math
import os

from const import ConstPlenty
from aruco import findArucoMarkers, detectAruco
from vision import detectRobot
from funcs import getDistanceBetweenPoints, getErrorByPoints, angleToPoint
from devices import Camera, Robot
import numpy as np
import cv2

const = ConstPlenty()
robot = Robot('10.128.73.116', 5005)
camera = Camera(index=2)

def saveImage(img, fileName='Camera.png'):
    cv2.imwrite(os.path.join(const.path.images, fileName), img)

def showImage(img, scale=2, winName='ImageScene'):
    shape = img.shape[:2]
    imgShow = cv2.resize(img, list(map(lambda x: int(x * scale), shape[::-1])))
    cv2.imshow(winName, imgShow)
    if cv2.waitKey(1) == 27:
        robot.stop()
        camera.release()
        raise ValueError('Exit by user')

def solve(debug=True):
    from nto.final import Task
    task = Task()

    task.start()
    route = eval(task.getTask())
    # route = [{'marker_id': 2}, {'marker_id': 55}, {'marker_id': 205}]
    print(route)
    saveImage(camera.read())
    resultPath = getResultPath(route, show=True, debug=debug)
    if debug: print('WAIT...')
    while cv2.waitKey(1) != 32: cv2.imshow('ImageScene', camera.read())
    if debug: print('DONE')
    driveToArucoMarkers(resultPath, speed=120, show=True, debug=debug)

    robot.stop()
    camera.release()
    task.stop()

def getResultPath(route, show=False, debug=False):
    camera.setArucoSettings()
    markerCorners, markerIds = findArucoMarkers(camera, show=show)
    arucoPositions = detectAruco(camera.read(), markerCorners, markerIds, threshold=50)
    if debug: print(f'[ARUCO_POSITIONS]: {arucoPositions}')
    resultPath = []
    for aruco in route:
        markerId = aruco['marker_id']
        if f'p_{markerId}' in arucoPositions:
            resultPath.append(arucoPositions[f'p_{markerId}'])
    if debug: print(f'[RESULT_PATH]: {resultPath}')
    return resultPath

def driveForwardToPoint(posAruco, speed, show=False, debug=False):
    robot.resetRegulator()
    while True:
        imgScene = camera.read()
        centerRobot, directionPoint = detectRobot(imgScene)
        if not centerRobot or not directionPoint: continue
        distance = getDistanceBetweenPoints(centerRobot, posAruco)
        if debug: print(f'[DISTANCE]: {distance}')
        if abs(distance) < 7: break
        error = getErrorByPoints(directionPoint, posAruco, centerRobot)
        if debug: print(f'[ERROR ANGLE]: {error}, {math.degrees(error)}')
        robot.angleRegulator(error, speed)
        if show:
            imgShow = imgScene.copy()
            cv2.line(imgShow, list(map(int, directionPoint)), list(map(int, centerRobot)), (0, 0, 255), 2)
            cv2.line(imgShow, list(map(int, centerRobot)), list(map(int, posAruco)), (255, 0, 0), 2)
            showImage(imgShow)
    robot.bstop()

def driveRotateToAngle(angleAruco, angleLimit, show=False, debug=False):
    imgScene = camera.read()
    centerRobot, directionPoint = detectRobot(imgScene, show=show)
    directionArucoPoint = angleToPoint(centerRobot, angleAruco, d=35)
    flag = True
    while True:
        imgScene = camera.read()
        centerRobot, directionPoint = detectRobot(imgScene)
        if not centerRobot or not directionPoint: continue
        error = getErrorByPoints(directionPoint, directionArucoPoint, centerRobot)
        if debug: print(f'[ERROR ANGLE]: {error}')
        if abs(error) < math.radians(angleLimit): break
        if error > 0:
            robot.turnRight(40)
            robot.turnLeft(-38)
            flag = True
        else:
            robot.turnRight(-40)
            robot.turnLeft(38)
            flag = False
        if show:
            imgShow = imgScene.copy()
            cv2.line(imgShow, list(map(int, directionPoint)), list(map(int, centerRobot)), (0, 0, 255), 2)
            cv2.line(imgShow, list(map(int, centerRobot)), list(map(int, directionArucoPoint)), (255, 0, 0), 2)
            cv2.circle(imgShow, list(map(int, directionArucoPoint)), 3, (0, 255, 0), -1)
            showImage(imgShow)
    if flag:
        robot.turnRight(-40)
        robot.turnLeft(38)
    else:
        robot.turnRight(40)
        robot.turnLeft(-38)
    lastTime = time.time() + 0.07
    while lastTime > time.time(): pass
    robot.turnRight(120)
    robot.turnLeft(120)
    lastTime = time.time() + 0.06
    while lastTime > time.time(): pass
    robot.stop()

def driveToArucoMarkers(path, speed, show=False, debug=False):
    camera.setDefaultSettings()
    for numAruco, arucoMarker in enumerate(path):
        posAruco, angleAruco = arucoMarker
        if debug: print(f'[ARUCO]: {numAruco} | {arucoMarker}')
        if debug: print('SEARCHING ROBOT...')
        while True:
            imgScene = camera.read()
            centerRobot, directionPoint = detectRobot(imgScene, show=show)
            if centerRobot and directionPoint: break
            if show: showImage(imgScene)
        if debug: print('FORWARD')
        driveForwardToPoint(posAruco, speed, show, debug)
        time.sleep(2)
        if debug: print('ROTATE')
        driveRotateToAngle(angleAruco, angleLimit=6, show=show, debug=debug)
        if debug: print('DONE')
        time.sleep(2)
        if debug: print('ROTATE 360')
        robot.rotate360()
        robot.bstop()
        time.sleep(2)

if __name__ == '__main__':
    solve()