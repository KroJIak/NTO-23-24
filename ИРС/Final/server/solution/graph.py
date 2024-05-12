import json


class Line:
    def __init__(self, id, startPos=None, endPos=None):
        self.id = id
        self.startPos = startPos
        self.endPos = endPos
        self.points = []

    def addPoint(self, point):
        if not self.startPos:
            self.startPos = point
        self.endPos = point
        self.points.append(point)

    def to_dict(self):
        return {
            "id": self.id,
            "startPos": self.startPos.id,
            "endPos": self.endPos.id,
            "points": [point.id for point in self.points]  # Convert points to dictionaries
        }

    @staticmethod
    def from_dict(data, lines_data):
        line_id = data["id"]
        start_pos = data["startPos"]
        end_pos = data["endPos"]
        points = data["points"]  # Deserialize points from dictionaries
        line = Line(line_id, start_pos, end_pos)

        for i in lines_data[line_id]:
            line.addPoint(i)
            i.line = line

        return line


class Point:
    def __init__(self, id, pos, line=None, isCrossroad=False, isAruco=False, arucoAngle=None, neighbours=[]):
        self.id = id
        self.pos = pos
        self.line = line
        self.isCrossroad = isCrossroad
        self.isAruco = isAruco
        self.arucoAngle = arucoAngle
        self.isEnd = False
        if not neighbours:
            self.neighbours = []
        else:
            self.neighbours = neighbours

    def addNeighbour(self, point):
        self.neighbours.append(point)

    def isNeighbour(self, point):
        return point in self.neighbours

    def merge(self, point):  # Слияние двух точек (перекрестков)
        self.pos = ((self.pos[0] + point.pos[0]) // 2, (self.pos[1] + point.pos[1]) // 2)
        self.neighbours += point.neighbours

    def to_dict(self):
        return {
            "id": self.id,
            "pos": self.pos,
            "line": self.line.id if self.line else None,
            "isCrossroad": self.isCrossroad,
            "isAruco": self.isAruco,
            "arucoAngle": self.arucoAngle,
            "isEnd": self.isEnd,
            "neighbours": [neighbour.id for neighbour in self.neighbours]
        }

    @staticmethod
    def from_dict(data):
        point_id = str(data["id"])
        pos = data["pos"]
        line_id = data["line"]
        is_crossroad = data["isCrossroad"]
        is_aruco = data["isAruco"]
        aruco_angle = data["arucoAngle"]
        is_end = data["isEnd"]
        neighbour_ids = [str(i) for i in data["neighbours"]]

        point = Point(point_id, tuple(pos), None, is_crossroad, is_aruco, aruco_angle, neighbour_ids)

        # if line:
        #     line.addPoint(point)
        return point, line_id
    

def serialize(points, dictAruco, filename="data.json"):
    points = points.values()
    res = {"points": [], "lines": [], "dictAruco": dictAruco}
    lines = set()
    for i in points:
        res["points"] += [i.to_dict()]
        if i.line:
            lines.add(i.line)

    for i in lines:
        res["lines"] += [i.to_dict()]
    with open(filename, 'w') as json_file:
        json.dump(res, json_file, indent=4)


def deserialize(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        points = {}
        lines_data = {}
        for i in data["points"]:
            point, line_id = Point.from_dict(i)
            lines_data[line_id] = lines_data.get(line_id, []) + [point]
            points[point.id] = point

        for i in data["lines"]:
            Line.from_dict(i, lines_data)
        
        dictAruco = data["dictAruco"]
        for i in dictAruco.values():
            i[0] = tuple(i[0])
            for j in range(len(i[1])):
                i[1][j] = tuple(i[1][j])

        
        for i in points.values():
            new_neigh = []
            for j in range(len(i.neighbours)):
                try:
                    new_neigh += [points[i.neighbours[j]]]
                except KeyError:
                    pass
            i.neighbours = new_neigh

        return points, dictAruco
    

# if __name__ == "__main__":
#     line1 = Line(1)
#     line2 = Line(2)
#     point1 = Point(1, (0, 0), line1)
#     point2 = Point(2, (1, 1), line1)
#     point3 = Point(3, (2, 2))

#     # Добавление точек к линиям
#     line1.addPoint(point1)
#     line1.addPoint(point2)
#     line2.addPoint(point3)

#     # Сериализация в JSON
#     serialize({point1.id: point1, point2.id: point2, point3.id: point3}, "data.json")

#     # Десериализация из JSON
#     res = deserialize("data.json")

