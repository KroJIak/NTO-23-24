import cv2
import numpy as np
from math import sqrt, pi
# [Константы]. Здесь записаны значения, которые не изменяются в течение всей работы программы,
# такие как сила размытия (для определния фигур), ограничения каждого из цвета (для определения контуров),
# перевод каждого цвета на русский и шрифт всех текстов на изображении.
DEAFULT_BLUR = 7
COLORS = {
    'red': [(122, 97, 140), (255, 223, 255), 10],
    'orange': [(0, 52, 155), (18, 255, 255), DEAFULT_BLUR],
    'yellow': [(18, 35, 121), (76, 255, 255), DEAFULT_BLUR],
    'green': [(34, 36, 0), (78, 255, 255), DEAFULT_BLUR],
    'lightBlue': [(37, 160, 0), (144, 255, 255), DEAFULT_BLUR],
    'blue': [(79, 65, 61), (147, 255, 156), DEAFULT_BLUR],
    'purple': [(133, 52, 76), (166, 111, 162), DEAFULT_BLUR]
}
TRANLASE_COLORS = {
    'red': 'Красный',
    'orange': 'Оранжевый',
    'yellow': 'Желтый',
    'green': 'Зеленый',
    'lightBlue': 'Голубой',
    'blue': 'Синий',
    'purple': 'Фиолетовый'
}
TEXT_FONT = cv2.FONT_HERSHEY_COMPLEX

# функция нахождения центра контура
def findContourCenter(cnt):
    cx, cy = None, None
    moment = cv2.moments(cnt)
    if moment['m00'] != 0:
        cx = int(moment['m10'] / moment['m00'])
        cy = int(moment['m01'] / moment['m00'])
    return (cx, cy)

# функция для слеивания двух изображений с прозрачностью
def alphaMergeImage4D(background, foreground):
    if foreground is None: return background
    resultImg = background.copy()
    alpha = foreground[:, :, 3] / 255.0
    resultImg[:, :, 0] = foreground[:, :, 0] * alpha + background[:, :, 0] * (1 - alpha)
    resultImg[:, :, 1] = foreground[:, :, 1] * alpha + background[:, :, 1] * (1 - alpha)
    resultImg[:, :, 2] = foreground[:, :, 2] * alpha + background[:, :, 2] * (1 - alpha)
    return resultImg

# добавление прозрачности изображению
def addAlphaInImage(img):
    resultImg = getZero4DImage(img.shape)
    resultImg[:, :, :3] = img.copy()
    resultImg[:, :, 3] = 255
    return resultImg

# создание пустого черного изображения с прозрачностью
def getZero4DImage(shape):
    height, width = shape[:2]
    zeroImg = np.zeros((height, width, 4), dtype=np.uint8)
    return zeroImg

# Функция для получения названия цвета, центра фигуры, его радиуса и цвета
# Стандартные значения: coefApprox - коэффициент аппроксимации; cntRange - ограничение по площади контура; approxRange - ограничение по количеству вершин конутра после аппроксимации
def detectCircle(img, coefApprox=0.03, cntRange=(5800, 7300), approxRange=(6, 10)):
    circles = {clr: 0 for clr in COLORS}
    lastColor, circleCenter = None, None
    radius = None
    colorN = None
    for clr, cdata in COLORS.items():
        # получение всех контуров по цвету
        copyImg = img.copy()
        imgHSV = cv2.cvtColor(copyImg, cv2.COLOR_BGR2HSV)
        imgBinary = cv2.inRange(imgHSV, cdata[0], cdata[1])
        imgBlur = cv2.blur(imgBinary, ksize=(cdata[2], cdata[2]))
        contours, _ = cv2.findContours(imgBlur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # сортировка контура по площади и исключение неподходящих контуров
        sortedContours = [cnt for cnt in sorted(contours, key=cv2.contourArea)
                          if cntRange[0] <= cv2.contourArea(cnt) <= cntRange[1]]
        for cnt in sortedContours:
            epsilon = coefApprox * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            # выборка фигур, только с определенным количеством вершин после аппроксимации
            if approxRange[0] <= len(approx) <= approxRange[1]:
                radius = round(sqrt(cv2.contourArea(cnt) / pi))
                lastColor = clr
                circleCenter = findContourCenter(cnt)
                colorN = copyImg[circleCenter[1], circleCenter[0]]
                circles[clr] += 1
    allCount = sum(list(circles.values()))
    if allCount > 1: return None, None, None, None
    if allCount == 1: return lastColor, circleCenter, radius, colorN
    return None, None, None, None

def drawInfo(img, color):
    resultImg = img.copy()
    # отрисовка информации справа снизу изображения
    resultImg[-70:, -700:, :] = 200
    nameColor = TRANLASE_COLORS[color] if color else None
    cv2.putText(resultImg, f'Отслеживаемый цвет объекта: {nameColor}', (resultImg.shape[1]-680, resultImg.shape[0]-30), TEXT_FONT, 0.8, (0, 0, 0), 2)
    return resultImg

# отрисовка траектории
def drawTrajectory(img, circleTrajectory, radius, colorN, pr=30):
    zeroImg = getZero4DImage(img.shape)
    for i, trj in enumerate(circleTrajectory):
        colorNN = tuple([int(x) for x in colorN] + [255 * max(10, i-len(circleTrajectory)+pr) / pr])
        cv2.circle(zeroImg, trj, radius, colorNN, -1)
    for i in range(len(circleTrajectory) - 1):
        cv2.line(zeroImg, circleTrajectory[i], circleTrajectory[i + 1], (246, 39, 182, 255), 2)
        cv2.circle(zeroImg, circleTrajectory[i], 2, (230, 23, 160, 255))
    cv2.circle(zeroImg, circleTrajectory[-1], 2, (230, 23, 160, 255))
    return zeroImg

# главная функция
def main():
    # настройка камеры: разрешение, метод считывания видеопотока, количество кадров в секунду, настройка фокуса
    cap = cv2.VideoCapture(2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOCUS, 0)

    # предустановки
    firstTrackedColor = ''
    firstRadius = None
    firstColorN = None
    circleTrajectory = []
    success, img = cap.read()
    zeroImg = getZero4DImage(img.shape)
    # основной цикл
    while True:
        success, img = cap.read()
        trackedColor, circleCenter, radius, colorN = detectCircle(img)
        if firstTrackedColor == '' and trackedColor is not None:
            firstTrackedColor = trackedColor
            firstRadius = radius
            firstColorN = colorN
        if trackedColor == firstTrackedColor:
            circleTrajectory.append(circleCenter)
            zeroImg = drawTrajectory(img, circleTrajectory, firstRadius, firstColorN)
        img = alphaMergeImage4D(img, zeroImg)
        resultImg = drawInfo(img, firstTrackedColor)
        cv2.imshow('Image', resultImg)
        if cv2.waitKey(1) == 27: break # выход по кнопке ESC

if __name__ == '__main__':
    main()