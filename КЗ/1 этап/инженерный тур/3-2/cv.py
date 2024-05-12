import cv2
import os
from copy import copy

path = 'data/train/'
listFiles = os.listdir(path)

def func():
    res = {
        'wolf': [],
        'fox': [],
        'pig': [],
        'rabbit': [],
        'deer': []
    }
    for file in listFiles:
        lastRes = {key:[elm for elm in res[key]] for key in res}
        while True:
            cv2.imshow('Image', cv2.imread(path+file))
            match cv2.waitKey(1):
                case 27:
                    return file, res
                case 99:
                    res['wolf'].append(file)
                    print('wolf')
                case 118:
                    res['fox'].append(file)
                    print('fox')
                case 98:
                    res['pig'].append(file)
                    print('pig')
                case 110:
                    res['rabbit'].append(file)
                    print('rabbit')
                case 109:
                    res['deer'].append(file)
                    print('deer')
                case 122:
                    res = copy(lastRes)
                    print('откат')
                case 32: break


lastFile, res = func()
print(lastFile)
print(res)

cv2.destroyAllWindows()