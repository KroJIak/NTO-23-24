
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f'[Vector] x: {self.x} y: {self.y}'

class Velocity(Vector):
    def __int__(self, x: float, y: float):
        super().__init__(x, y)

    def __str__(self):
        return f'[Velocity] x: {self.x} y: {self.y}'

class Position:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f'[Position] x: {self.x} y: {self.y}'


class Balloon:
    def __init__(self, pos: Position, velocity: Velocity, radius: float, color: tuple):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.velocity = velocity

    def __str__(self):
        return f'[Balloon] pos: {self.pos.x, self.pos.y} radius: {self.radius} color: {self.color} velocity: {self.velocity}'
