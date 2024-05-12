import cv2

def save(img):
    pass


def markupPositions(img, contours, markupArray):
    img = img.copy()
    cv2.drawContours(img, contours, -1, (255, 0, 0), 1)
    [cv2.putText(img, str(i), (center[0] - 4, center[1] - 4), cv2.FONT_HERSHEY_COMPLEX, 0.3, (100, 0, 255),
                    0)
        for i, center in enumerate(markupArray)]
    save(img)


def dictAruco(img, aruco):
    img = img.copy()
    for key, val in aruco.items():
        cv2.putText(img, key, val, cv2.FONT_HERSHEY_COMPLEX, 1, (100, 0, 255), 2)
    save(img)


def robotPos(img, pos, r=10):
    img = img.copy()
    cv2.circle(img, pos, r)
    save.img()


def roadLines(img, lines):
    imgLines = img.copy()
    colorA = (0, 0, 255)
    colorB = (0, 100, 255)
    isA = True
    for line in lines:
        for i in range(len(line) - 1):
            if isA:
                color = colorA
            else:
                color = colorB
            isA = not isA
            cv2.line(imgLines, line[i], line[i + 1], color, 2)
    save(imgLines)

def extendLines(img, lines):
    return roadLines(img, lines)


def saveGraph(img, points):
    imgLines = img.copy()
    # рисуем граф
    for point in points.values():
        for neighbour in point.neighbours:
            cv2.line(imgLines, point.pos, neighbour.pos, (76, 235, 23), 2)
            cv2.circle(imgLines, point.pos, 5, (153, 0, 204), 2)

    save(imgLines)