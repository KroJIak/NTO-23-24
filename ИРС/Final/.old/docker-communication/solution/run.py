from fastapi import FastAPI
from vision import *
import os
from const import ConstPlenty

app = FastAPI()

def saveImage(img):
    cv2.imwrite(os.path.join(const.path.images, f'Camera_{1}.png'), img)

@app.get("/robot/pos")
def robotPos():
    _, imgScene = cap.read()
    centerRobot, directionPoint = detectRobot(imgScene)
    print(centerRobot, directionPoint)
    if centerRobot is None or directionPoint is None: return
    cv2.circle(imgScene, centerRobot, 3, (255, 255, 255), -1)
    cv2.circle(imgScene, directionPoint, 3, (255, 255, 255), -1)
    saveImage(imgScene)
    positions = '0,0,0;'
    positions += ','.join(list(map(str, centerRobot))+['0'])+';'
    positions += ','.join(list(map(str, directionPoint))+['0'])+';'
    return positions

def runWebhook():
    import uvicorn
    global const, cap
    const = ConstPlenty()
    cap = cv2.VideoCapture(2)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 20)
    cap.set(cv2.CAP_PROP_FOCUS, 0)
    cap.set(cv2.CAP_PROP_SATURATION, 0)

    uvicorn.run("run:app",
                reload=False,
                host="0.0.0.0",
                port=5400,)