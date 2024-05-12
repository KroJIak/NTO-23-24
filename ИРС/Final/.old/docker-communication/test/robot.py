import cv2
from docker.solution.vision import *

img = cv2.imread('../solution/images/Camera_01.png')
centerRobot, directionPoint = detectRobot(img, show=True)
print(centerRobot, directionPoint)