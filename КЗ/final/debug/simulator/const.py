
class Color:
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (0, 0, 255)
        self.green = (0, 255, 0)
        self.blue = (255, 0, 0)
        self.yellow = (0, 255, 255)

class Wall:
    def __init__(self):
        self.thickness = 10

class ConstPlenty:
    def __init__(self):
        self.color = Color()
        self.DT = 10
        self.wall = Wall()