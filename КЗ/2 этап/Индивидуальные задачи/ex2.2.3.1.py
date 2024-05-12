pos1 = tuple(map(float, input().split()))
pos2 = tuple(map(float, input().split()))
speed1 = tuple(map(float, input().split()))
speed2 = tuple(map(float, input().split()))
needTime = 10

class Line():
    def __init__(self, pos=None, speed=None):
        self.speed = speed
        self.findK(pos)
        self.findB(pos)

    def findK(self, pos):
        if pos is None:
            self.k = None
            return
        x1, y1 = pos
        vx, vy = self.speed
        x2, y2 = x1 + vx, y1 + vy

        if (x1 - x2) == 0:
            self.k = None
            self.xConst = x1
            return
        self.k = (y1 - y2) / (x1 - x2)

    def findB(self, pos):
        if self.k is None:
            self.b = None
            return
        x, y = pos
        self.b = y - self.k * x

    def getFunc(self, x):
        return self.k * x + self.b

    def getNextPoint(self, pos, nextTime):
        x, y = pos
        x += self.speed[0] * nextTime
        y += self.speed[1] * nextTime
        return [x, y]

def findCommonPos(line1, line2):
    if line1.k is None and line2.k is None: return None
    elif line1.k == line2.k and line1.b != line2.b: return None
    elif line1.k is None:
        x = line1.xConst
        y = line2.getFunc(x)
    elif line2.k is None:
        x = line2.xConst
        y = line1.getFunc(x)
    else:
        x = (line2.b - line1.b) / (line1.k - line2.k)
        y = line1.getFunc(x)
        if y != line2.getFunc(x): return None
    return (x, y)

line1 = Line(pos1, speed1)
line2 = Line(pos2, speed2)

commonPos = findCommonPos(line1, line2)
if commonPos is None:
    print([pos1[0] + (speed1[0] * needTime), pos1[1] + (speed1[1] * needTime)],
          [pos2[0] + (speed2[0] * needTime), pos2[1] + (speed2[1] * needTime)])
    exit(0)

lineh = Line()
lineh.k = (-1 / line1.k)
lineh.b = line1.b
rightX, leftX = commonPos[0] + 1, commonPos[0] - 1
rightY, leftY = lineh.getFunc(rightX), lineh.getFunc(leftX)
print(rightX, rightY)
print(leftX, leftY)
timeBefore = (commonPos[0] - pos1[0]) / speed1[0]
print(timeBefore)
print(line2.getNextPoint(commonPos, needTime-timeBefore), line1.getNextPoint(commonPos, needTime-timeBefore))

'''
-5.5 0
5.5 0
1.0 1.0
-1.0 1.0
'''