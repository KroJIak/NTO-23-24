import cv2

# найти расстояние между двумя точками
def distanceBetweenPositions(pos1, pos2) -> float:
    dist = ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**0.5
    return dist

# найти центр контура
def findContourCenter(cnt):
    cx, cy = None, None
    moment = cv2.moments(cnt)
    if moment['m00'] != 0:
        cx = int(moment['m10'] / moment['m00'])
        cy = int(moment['m01'] / moment['m00'])
    return (cx, cy)
