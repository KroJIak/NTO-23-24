import cv2

# [Константы]. Здесь записаны значения, которые не изменяются в течение всей работы программы,
# такие как сила размытия (для определния фигур), ограничения каждого из цвета (для определения контуров),
# перевод каждого цвета на русский и текст инструкции с шрифтом этого текста.
DEAFULT_BLUR = 7
COLORS = {
    'red': [(122, 97, 140), (255, 223, 255), 10],
    'orange': [(0, 52, 155), (18, 255, 255), DEAFULT_BLUR],
    'yellow': [(18, 35, 121), (76, 255, 255), DEAFULT_BLUR],
    'green': [(34, 36, 0), (78, 255, 255), DEAFULT_BLUR],
    'lightBlue': [(37, 160, 0), (144, 255, 255), DEAFULT_BLUR],
    'blue': [(79, 65, 61), (147, 255, 156), DEAFULT_BLUR],
    'purple': [(133, 52, 76), (166, 111, 162), DEAFULT_BLUR],
    'black': [(28, 10, 0), (162, 70, 89), DEAFULT_BLUR]
}
TRANLASE_COLORS = {
    'red': 'Красный',
    'orange': 'Оранжевый',
    'yellow': 'Желтый',
    'green': 'Зеленый',
    'lightBlue': 'Голубой',
    'blue': 'Синий',
    'purple': 'Фиолетовый',
    'black': 'Черный'
}
TEXT_FONT = cv2.FONT_HERSHEY_COMPLEX
WARN_TEXT = 'Добро пожаловать! \nЧтобы посчитать количетсво \nфигур круглой формы определенных цветов \n(красный, оранжевый, желтый, зеленый, \nголубой, синий, коричневый, черный), \nпродемонстрируйте их перед вашей камерой.'

# Функция для получения словаря с количеством каждого цвета. Принимает изображение.
# Стандартные значения: coefApprox - коэффициент аппроксимации; cntRange - ограничение по площади контура; approxRange - ограничение по количеству вершин конутра после аппроксимации
def getCircles(img, coefApprox=0.03, cntRange=(5800, 7300), approxRange=(6, 10)):
    circles = {clr: 0 for clr in COLORS}
    for clr, cdata in COLORS.items():
        # получение всех контуров по цвету
        copyImg = img.copy()
        imgHSV = cv2.cvtColor(copyImg, cv2.COLOR_BGR2HSV)
        imgBinary = cv2.inRange(imgHSV, cdata[0], cdata[1])
        imgBlur = cv2.blur(imgBinary, ksize=(cdata[2], cdata[2]))
        contours, _ = cv2.findContours(imgBlur, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # сортировка контура по площади и исключение неподходящих контуров
        sortedContours = [cnt for cnt in sorted(contours, key=cv2.contourArea)
                          if cntRange[0] <= cv2.contourArea(cnt) <= cntRange[1]]
        for cnt in sortedContours:
            epsilon = coefApprox * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            # выборка фигур, только с определенным количеством вершин после аппроксимации
            if approxRange[0] <= len(approx) <= approxRange[1]:
                circles[clr] += 1
    return circles

def drawInfo(img, circles, step=40):
    resultImg = img.copy()
    # общее количетсво фигур на изображении
    allCount = sum(list(circles.values()))
    if allCount > 0:
        # отрисовка информации справа снизу изображения
        resultImg[-400:, -330:, :] = 200
        cv2.putText(resultImg, f'Всего: {allCount}', (resultImg.shape[1]-300, resultImg.shape[0]-350), TEXT_FONT, 1, (0, 0, 0), 2)
        for id, (clr, count) in enumerate(circles.items(), start=1): cv2.putText(resultImg, f'{TRANLASE_COLORS[clr]}: {count}',
                                                                   (resultImg.shape[1]-300, resultImg.shape[0]-350+(id*step)), TEXT_FONT, 1, (0, 0, 0), 2)
    else:
        # отрисовка инструкции по середине изображения
        height, weigth = (resultImg.shape[0] // 6), (resultImg.shape[1] // 6)
        resultImg[height:-height, weigth:-weigth, :] = 200
        for id, cutText in enumerate(WARN_TEXT.split('\n')):
            cv2.putText(resultImg, cutText, (weigth + 20, height + 120 + (id*step)), TEXT_FONT, 1, (0, 0, 0), 2)
    return resultImg

# главная функция
def main():
    # настройка камеры: разрешение, метод считывания видеопотока, количество кадров в секунду, настройка фокуса
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOCUS, 0)

    # основной цикл
    while True:
        success, img = cap.read()
        circles = getCircles(img)
        resultImg = drawInfo(img, circles)
        cv2.imshow('Image', resultImg)
        if cv2.waitKey(1) == 27: break # выход по кнопке ESC

if __name__ == '__main__':
    main()