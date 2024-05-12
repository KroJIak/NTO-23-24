
# класс вектора
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f'[Vector] x: {self.x} y: {self.y}'

# класс скорости, дочерний класс вектора
class Velocity(Vector):
    def __int__(self, x: float, y: float):
        super().__init__(x, y)

    def __str__(self):
        return f'[Velocity] x: {self.x} y: {self.y}'

# класс позиции в пространстве
class Position:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f'[Position] x: {self.x} y: {self.y}'

# класс игрового объекта - кружочек
class Balloon:
    def __init__(self, pos: Position, velocity: Velocity, radius: float, color: tuple):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.velocity = velocity

    def __str__(self):
        return f'[Balloon] pos: {self.pos.x, self.pos.y} radius: {self.radius} color: {self.color} velocity: {self.velocity}'

# класс игрового объекта - граница поля
class BinaryBorder:
    def __init__(self, startPos: Position, endPos: Position, thickness: float, color: tuple):
        self.startPos = startPos
        self.endPos = endPos
        self.thickness = thickness
        self.color = color

    def __str__(self):
        return f'[BinaryBorder] startPos: {self.startPos} endPos: {self.endPos} thickness: {self.thickness} color: {self.color}'