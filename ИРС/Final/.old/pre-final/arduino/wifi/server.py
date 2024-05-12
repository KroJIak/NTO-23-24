from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from threading import Thread

app = FastAPI()

@app.get('/get/angle/')
async def getAngle():
    pass

def runUvicorn():
    uvicorn.run('host:app', host='localhost', port=2468, workers=10)

def turnOnServer():
    uvicornThread = Thread(target=runUvicorn)
    uvicornThread.start()