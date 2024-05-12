from modules.utils import setSampleData

data = []
while True:
    imageString = input()
    if imageString == 'stop': break
    robotPos = list(map(int, input().split()))
    countPoints = int(input())
    mainPoints = eval(input())
    data.append(dict(imageString=imageString, robotPos=robotPos,
                countPoints=countPoints, mainPoints=mainPoints))

setSampleData(data)