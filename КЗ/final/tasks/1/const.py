
# константы

class Color:
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (0, 0, 255)
        self.green = (0, 255, 0)
        self.blue = (255, 0, 0)
        self.yellow = (0, 255, 255)

class ArucoIds:
    def __init__(self):
        self.leftUp = 7
        self.rightDown = 10

class Border:
    def __init__(self):
        self.leftUp = (0, 0)
        self.rightDown = (float('inf'), float('inf'))
        self.realArucoSize = 60
        self.color = 20

class Text:
    def __init__(self):
        self.start = 'Нажмите любую кнопку, чтобы начать'
        self.restart = 'Вы проиграли, Нажмите любую кнопку, чтобы перезапустить'
        self.calibration = 'Для калибровки нажмите на углы проектора'
        self.space = 'При нажатии на пробел откроется полноэкранный режим'

class Camera:
    def __init__(self):
        self.index = 0

class Balloon:
    def __init__(self):
        self.radius = 120
        self.createPeriod = 3
        self.speedRange = (5, 9)

class Game:
    def __init__(self):
        self.maxCountBalloons = 5

class ConstPlenty:
    def __init__(self):
        self.color = Color()
        self.border = Border()
        self.arucoIds = ArucoIds()
        self.text = Text()
        self.camera = Camera()
        self.balloon = Balloon()
        self.game = Game()
        self.DT = 10