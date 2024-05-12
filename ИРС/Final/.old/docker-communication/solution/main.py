import socket
import os
from const import ConstPlenty
from vision import *
from aruco import findArucoMarkers, detectAruco
from fastapi import FastAPI
import cv2
import time
from run import runWebhook

from nto.final import Task

const = ConstPlenty()
task = Task()

class Robot:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message):
        self.sock.sendto(message, (self.ip, self.port))

    def sendPath(self, path):
        strPath = ';'.join([','.join(list(map(str, pos))) for pos in path])+';'
        print(strPath)
        self.send(strPath.encode('utf-8'))

cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 20)
cap.set(cv2.CAP_PROP_FOCUS, 0)
cap.set(cv2.CAP_PROP_SATURATION, 0)

## Здесь должно работать ваше решение
def solve():
    task.start()
    robot = Robot('10.128.73.116', 5005)
    saveImage()
    print(task.getTask())
    path = getResultPath(eval(task.getTask()))
    robot.sendPath(path)
    cap.release()
    runWebhook()
    task.stop()

def saveImage():
    _, img = cap.read()
    cv2.imwrite(os.path.join(const.path.images, f'Camera_{0}.png'), img)

def getResultPath(route):
    _, imgScene = cap.read()
    markerCorners, markerIds = findArucoMarkers(imgScene, show=False)
    arucoPositions = detectAruco(imgScene, markerCorners, markerIds)
    print(len(arucoPositions), arucoPositions)
    resultPath = []
    route = [{'marker_id': 2}, {'marker_id': 55}, {'marker_id': 205}]
    for aruco in route:
        markerId = aruco['marker_id']
        if f'p_{markerId}' in arucoPositions:
            resultPath.append(arucoPositions[f'p_{markerId}'])
    print(resultPath)
    return resultPath




if __name__ == '__main__':
    solve()