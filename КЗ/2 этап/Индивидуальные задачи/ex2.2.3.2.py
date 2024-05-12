from math import hypot

pos1 = list(map(float, input().split()))
pos2 = list(map(float, input().split()))
speed1 = list(map(float, input().split()))
speed2 = list(map(float, input().split()))
needTime = 10

flag = False
for i in range(needTime):
    pos1 = [pos1[0] + speed1[0], pos1[1] + speed1[1]]
    pos2 = [pos2[0] + speed2[0], pos2[1] + speed2[1]]
    dist = hypot(pos2[0]-pos1[0], pos2[1]-pos1[1])
    if round(dist, 2) == 1 and not flag:
        flag = True
        speed1, speed2 = speed2, speed1
print(f'{pos1}, {pos2}')
'''
-5.5 0
5.5 0
1.0 1.0
-1.0 1.0
'''