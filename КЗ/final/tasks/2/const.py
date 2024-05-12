
### константы

# цвета в формате BGR
class Color:
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (0, 0, 255)
        self.green = (0, 255, 0)
        self.blue = (255, 0, 0)
        self.yellow = (0, 255, 255)

# границы углов изображения проекции проектора
class ScreenBorder:
    def __init__(self):
        self.leftUp = (0, 0)
        self.rightDown = (float('inf'), float('inf'))

# свойства игрового объекта - граница поля
class BinaryBorder:
    def __init__(self, color: tuple):
        self.color = color
        self.thickness = 8

# свойства игрового объекта - корзина
class Basket:
    def __init__(self, color: tuple):
        self.color = color
        self.thickness = 4

# текста
class Text:
    def __init__(self):
        self.start = 'Нажмите любую кнопку, чтобы начать'
        self.restart = 'Вы выйграли! Нажмите любую кнопку, чтобы перезапустить'
        self.calibration = 'Для калибровки нажмите на углы проектора'
        self.space = 'При нажатии на пробел откроется полноэкранный режим'
        self.insturction = 'Нужно загнать шарик в корзину при помощи линий, которые вы рисуете маркерами'
        self.insturction_2 = 'Esc - выйти R - пересоздать шарик'
        self.score = 'Счет'
        self.win = 'Вы молодец! Стирайте все линии и нажмите любую кнопку'

# свойства игрового объекта - кружочек
class Balloon:
    def __init__(self):
        self.radius = 60
        self.radiusOffset = 15
        self.speedRange = (3, 6)

# основной класс констант
class ConstPlenty:
    def __init__(self):
        self.color = Color()
        self.screenBorder = ScreenBorder()
        self.binaryBorder = BinaryBorder(self.color.red)
        self.basket = Basket(self.color.green)
        self.text = Text()
        self.balloon = Balloon()
        self.DT = 10