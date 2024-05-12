
import cv2
from const import ConstPlenty

const = ConstPlenty()

# проверить нажатие мыши
def checkMouse(event, x, y, flags, param):
    mousePos = (x, y)
    match event:
        case cv2.EVENT_LBUTTONDOWN:
            addCornerPoint(mousePos)

def showImage(img, nameWindow='Image'):
    cv2.imshow(nameWindow, img)
    match cv2.waitKey(1):
        case 27: exit(0)

def addCornerPoint(pos):
    global cornerPoints
    cornerPoints.append(pos)

def drawBorderPoints(img):
    resultImg = img.copy()
    for pos in cornerPoints:
        cv2.circle(resultImg, pos, 8, const.color.white, -1)
        cv2.circle(resultImg, pos, 5, const.color.green, -1)
    return resultImg

# Рисует текст в окне калибрации
def drawInstruction(img):
    resultImg = img.copy()
    cv2.putText(resultImg, const.text.calibration, (20, 40),
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
    return resultImg

# получить угловые точки проекции на стене от проектора
def getCameraCornerPoints(camera, nameWindowCamera='Camera'):
    global cornerPoints
    cornerPoints = []
    rawCameraImg = camera.readRaw()
    showImage(rawCameraImg, nameWindowCamera)
    cv2.setMouseCallback(nameWindowCamera, checkMouse)
    while len(cornerPoints) < 4:
        rawCameraImg = camera.readRaw()
        rawCameraImg = drawInstruction(rawCameraImg)
        rawCameraImg = drawBorderPoints(rawCameraImg)
        showImage(rawCameraImg, nameWindowCamera)
    resultCornerPoints = []
    for CCP in [(0, 0), (rawCameraImg.shape[1], 0), (0, rawCameraImg.shape[0]), (rawCameraImg.shape[1], rawCameraImg.shape[0])]:
        distances = [((CCP[0] - pnt[0])**2 + (CCP[1] - pnt[1])**2)**0.5 for pnt in cornerPoints]
        resultCornerPoints.append(cornerPoints[distances.index(min(distances))])
    cv2.destroyWindow(nameWindowCamera)
    return resultCornerPoints

# Получает углыы проектора
def getProjectorCornerPoints(windowSize):
    projectorCornerPoints = [(0, 0), (windowSize[0], 0), (0, windowSize[1]), tuple(windowSize)]
    return projectorCornerPoints