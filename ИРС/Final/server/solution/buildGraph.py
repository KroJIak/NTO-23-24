from graph import Line, Point
from algorithms import getDistanceBetweenPoints, getPosRightSideSegment

def addCrossroads(points, lines, dist):
    # PS тут много квадратичных сложностей, но концов точек меньше 200 штук, а перекрестков еще меньше
    # поэтому можно не париться

    startsEndsPoints = []
    for line in lines.values():
        startsEndsPoints.append(line.startPos)
        startsEndsPoints.append(line.endPos)

    # minDistBetweenLines = float('+inf')
    # for point1, point2 in combinations(startsEndsPoints, 2):
    #     minDistBetweenLines = min(getDistanceBetweenPoints(point1.pos, point2.pos), minDistBetweenLines)
    minRoadDist = float('+inf')
    for line in lines.values():
        if getDistanceBetweenPoints(line.points[0].pos, line.points[-1].pos) > dist:
            minRoadDist = min(minRoadDist, getDistanceBetweenPoints(line.points[0].pos, line.points[-1].pos))

    crossroads = []
    while startsEndsPoints:
        query = [startsEndsPoints.pop()]
        crossroad = []
        while query:
            point = query.pop()
            crossroad += [point]
            for i in range(len(startsEndsPoints) - 1, -1, -1):
                point2 = startsEndsPoints[i]
                if getDistanceBetweenPoints(point.pos, point2.pos) < minRoadDist * 0.9995:
                    query.append(point2)
                    startsEndsPoints.pop(i)

        # Если 2 точки принадлежат одной линии, то выбираем ту, которая ближе к остальным точкам
        # for point1 in crossroad:
        #     for point2 in crossroad:
        #         if point1 == point2: continue
        #         elif point1.line == point2.line:
        #             dist1 = sum([getDistanceBetweenPoints(point1.pos, point.pos) for point in crossroad])
        #             dist2 = sum([getDistanceBetweenPoints(point2.pos, point.pos) for point in crossroad])
        #             if dist1 < dist2:
        #                 crossroad.remove(point1)
        #             else:
        #                 crossroad.remove(point2)
        crossroads.append(crossroad)

    crossroadId = len(points) + 10000
    newCrossroads = []
    for crossroad in crossroads:
        x = round(sum([point.pos[0] for point in crossroad]) / len(crossroad))
        y = round(sum([point.pos[1] for point in crossroad]) / len(crossroad))
        pos = (x, y)
        point = Point(crossroadId, pos, isCrossroad=True, neighbours=crossroad)
        points[crossroadId] = point

        for p in crossroad:
            p.addNeighbour(point)

        crossroadId += 1
        newCrossroads.append(point)
    crossroads = newCrossroads

    # Если расстояние между 2 центрами меньше минимальной длины принадлежащих им линий, то соединяем их в один перекресток
    # to_merge = []
    # for point1 in crossroads:
    #     for point2 in crossroads:
    #         if point1 == point2 or getDistanceBetweenPoints(point1.pos, point2.pos) > 20: continue
    #         minDistance = float('+inf')
    #         for neighbour in point1.neighbours + point2.neighbours:
    #             dist = getDistanceBetweenPoints(neighbour.line.startPos.pos, neighbour.line.endPos.pos)
    #             minDistance = min(minDistance, dist)
    #         if minDistance * 1.1 > getDistanceBetweenPoints(point1.pos, point2.pos):
    #             to_merge.append((point1, point2))

    # print(to_merge)
    # for point1, point2 in to_merge:
    #     point1.merge(point2)
    #     points.pop(point2.id)
    #     crossroads.remove(point2)

    # # Удаляем крайние точки линий
    # print(len(points))
    # for line in lines.values():
    #     p1 = line.points.pop(0)
    #     p2 = line.points.pop(-1)
    #     line.startPos = line.points[0]
    #     line.endPos = line.points[-1]

    #     points.pop(p1.id)
    #     points.pop(p2.id)

    #     for point in p1.neighbours:
    #         point.neighbours.remove(p1)
    #         for point2 in p1.neighbours:
    #             if point2 == point: continue
    #             if point2 not in point.neighbours:
    #                 point.neighbours.append(point2)
    #                 point2.neighbours.append(point)
    #     for point in p2.neighbours:
    #         point.neighbours.remove(p2)
    #         for point2 in p2.neighbours:
    #             if point2 == point: continue
    #             if point2 not in point.neighbours:
    #                 point.neighbours.append(point2)
    #                 point2.neighbours.append(point)

    # print(len(points))

    return points


def getGraph(lines, distCrossroads=20):
    # Рефакторим данные, тк на данном этапе требуется двухсторонняя связь
    points = {}
    newLines = {}
    idLines = 0
    idPoints = 0
    for line in lines:
        newLine = Line(idLines)
        isFirst = True
        for pos in line:
            point = Point(idPoints, pos, newLine)
            points[idPoints] = point
            newLine.addPoint(point)
            if not isFirst:
                points[idPoints - 1].addNeighbour(point)
                point.addNeighbour(points[idPoints - 1])
            idPoints += 1
            isFirst = False
        newLines[idLines] = newLine
        idLines += 1
    lines = newLines

    points = addCrossroads(points, lines, distCrossroads)

    for line in lines.values():
        line.endPos.isEnd = True
        line.startPos.isEnd = True

    return points


def refactorGraph(points):
    crossroads = list(filter(lambda p: p.isCrossroad, points.values()))
    newPoints = {}
    congruence = {}
    idInt = 0
    for crossroad in crossroads:
        newCrossroad = Point(idInt, crossroad.pos, isCrossroad=True)
        newPoints[idInt] = newCrossroad
        congruence[crossroad.id] = newCrossroad
        idInt += 1

    for crossroad in crossroads:
        newCrossroad = congruence[crossroad.id]
        for point in crossroad.neighbours:
            last = crossroad
            cur = point
            lastNewPoint = newCrossroad
            first = True
            while True:
                if cur.isCrossroad:
                    lastNewPoint.addNeighbour(congruence[cur.id])
                    break
                if not first:
                    newPos = getPosRightSideSegment(last.pos, cur.pos)
                else:
                    newPos = cur.pos
                    first = False
                newPoint = Point(idInt, newPos)
                lastNewPoint.addNeighbour(newPoint)
                newPoints[idInt] = newPoint
                idInt += 1
                if cur.isCrossroad:
                    break
                for nxt in cur.neighbours:
                    if nxt != last:
                        last = cur
                        cur = nxt
                        lastNewPoint = newPoint
                        break

    return newPoints


def perpendicular_line(point_on_line, slope, distance=1):
    # Calculate the slope of the perpendicular line
    if slope == 0:  # If the slope of the original line is 0, perpendicular slope is undefined (infinity)
        perpendicular_slope = float('inf')
    else:
        perpendicular_slope = -1 / slope  # Slope of perpendicular line is negative reciprocal

    # Calculate coordinates of the new points
    x, y = point_on_line
    # Move the new points perpendicular to the original line
    if perpendicular_slope == float("+inf"):
        new_point1 = (x, y + distance)
        new_point2 = (x, y - distance)
    else:
        delta_x = distance / ((1 + perpendicular_slope ** 2) ** 0.5)
        delta_y = perpendicular_slope * delta_x
        new_point1 = (x + delta_x, y + delta_y)
        new_point2 = (x - delta_x, y - delta_y)

    # Return the equation of the perpendicular line in point-slope form (y - y1 = m(x - x1))
    return new_point1, new_point2


def slope_between_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x2 - x1 == 0:  # Avoid division by zero for vertical lines
        return float('inf')
    else:
        return (y2 - y1) / (x2 - x1)


def findIntersectionAruco(p1, p2, slope, distance=10):
    mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    return perpendicular_line(mid, slope, distance=distance)


def addArucos(points, arucos, mainPoints=[]):
    arUcoId2PointId = {}
    for point in mainPoints:
        if "marker_id" in point:
            arUcoId2PointId[f'p_{point["marker_id"]}'] = point["name"]
    print(arUcoId2PointId)
    counter = 0
    pointsList = list(points.values())
    for arucoId, aruco in arucos.items():
        pointsList.sort(key=lambda p: getDistanceBetweenPoints(p.pos, aruco[0]))

        if arucoId in arUcoId2PointId:
            pointId = arUcoId2PointId[arucoId]
        else:
            pointId = "unused_" + arucoId

        # Строим перпендикуляр к дороге
        closestPoint = pointsList[0]
        p1, p2 = list(sorted(aruco[1], key=lambda x: getDistanceBetweenPoints(closestPoint.pos, x)))[:2]
        mid_point = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        aruco = list(aruco)
        if getDistanceBetweenPoints(mid_point, aruco[0]) > 17:
            aruco[1] = tuple(map(lambda x: tuple([x[1], x[0]]), aruco[1]))
            p1, p2 = list(sorted(aruco[1], key=lambda x: getDistanceBetweenPoints(closestPoint.pos, x)))[:2]
        slope = slope_between_points(p1, p2)
        a, b = findIntersectionAruco(p1, p2, slope, distance=20)
        newPointPos = min(a, b, key=lambda x: getDistanceBetweenPoints(x, closestPoint.pos))

        neighbours = list(sorted(pointsList, key=lambda x: getDistanceBetweenPoints(x.pos, newPointPos)))[:2]
        if neighbours[0] in neighbours[1].neighbours:
            left = neighbours[1]
            right = neighbours[0]
        else:
            left = neighbours[0]
            right = neighbours[1]

        arucoPoint = Point(pointId, aruco[0], isAruco=True, arucoAngle=aruco[2])
        newPointPos = (round(newPointPos[0]), round(newPointPos[1])) 
        newPoint = Point(f"addedPoint_{counter}", newPointPos, neighbours=[right, arucoPoint])

        points[newPoint.id] = newPoint
        points[pointId] = arucoPoint

        left.neighbours += [newPoint]
        arucoPoint.neighbours = [newPoint]
        counter += 1
        # print(newPoint.neighbours)
        # print(arucoPoint.neighbours)
        # print(arucoPoint.id)
        # # Берем ближайшую точку:
        # closestPoint = pointsList[0]
        # arucoPoint = Point(pointId, aruco[0], isAruco=True, arucoAngle=aruco[1], neighbours=[closestPoint])
        # closestPoint.addNeighbour(arucoPoint)
        # points[pointId] = arucoPoint


        # # Берем 3 точки, сортируем по ходу движения
        # closest = pointsList[:3]
        # first = closest
        # for i in closest:
        #     for neighbour in i.neighbours:
        #         if neighbour in closest:
        #             first.remove(neighbour)
        # first = first[0]
        # closest2 = [first]
        # for i in range(2):
        #     closest2.append(closest2[-1].neighbours[0])
        # closest = closest2

        # arucoPoint = Point(pointId, aruco[0], isAruco=True, arucoAngle=aruco[1], neighbours=[closest[2]])
        # points[pointId] = arucoPoint
        # closest[0].addNeighbour(arucoPoint)

    return points

def addEmptyArUco(points, emptyArUco):
    counter = 1000
    pointsList = list(points.values())
    for aruco in emptyArUco:
        pointId = f"em_{counter}"
        pointsList.sort(key=lambda p: getDistanceBetweenPoints(p.pos, aruco[0]))
        closestPoint = pointsList[0]
        p1, p2 = list(sorted(aruco[1], key=lambda x: getDistanceBetweenPoints(closestPoint.pos, x)))[:2]
        slope = slope_between_points(p1, p2)
        a, b = findIntersectionAruco(p1, p2, slope, distance=20)
        newPointPos = min(a, b, key=lambda x: getDistanceBetweenPoints(x, closestPoint.pos))

        neighbours = list(sorted(pointsList, key=lambda x: getDistanceBetweenPoints(x.pos, newPointPos)))[:2]
        if neighbours[0] in neighbours[1].neighbours:
            left = neighbours[1]
            right = neighbours[0]
        else:
            left = neighbours[0]
            right = neighbours[1]

        arucoPoint = Point(pointId, aruco[0], isAruco=True, arucoAngle=aruco[1])
        newPointPos = (round(newPointPos[0]), round(newPointPos[1]))
        newPoint = Point(f"addedPoint_{counter}", newPointPos, neighbours=[right, arucoPoint])

        points[newPoint.id] = newPoint
        points[pointId] = arucoPoint

        left.neighbours = [newPoint]
        arucoPoint.neighbours = [newPoint]
        counter += 1
    return points


def deletePoints(points, x1, x2):
    res = {}
    deleted = []
    for key, val in points.items():
        if not x1 < val.pos[0] < x2:
            res[key] = val
        else:
            deleted += [val]
    for key, val in res.items():
        new_neigh = []
        visited = []
        for neigh in val.neighbours:
            if neigh in deleted:
                queue = [neigh]
                while queue:
                    cur = queue.pop()
                    new_neigh += [cur]
                    if cur in deleted:
                        for abc in cur.neighbours:
                            if abc not in visited:
                                queue += [abc]
                                visited += [abc]
        val.neighbours += new_neigh

    # listPoints = list(res.values())
    # for key, val in res.items():
    #     for i in val.neighbours:
    #         pass

    return res


def addPoints(points, addPoints):
    pointsList = list(points.values())
    for pointData in addPoints:
        if "coordinates" in pointData and pointData["name"] not in points:
            pointsList.sort(key=lambda p: getDistanceBetweenPoints(p.pos, tuple(pointData["coordinates"])))
            closest = pointsList[0]
            if closest.isCrossroad:
                newPoint = Point(pointData["name"], tuple(pointData["coordinates"]), neighbours=[closest])
                points[pointData["name"]] = newPoint
                closest.addNeighbour(newPoint)
            else:
                closest.pos = tuple(pointData["coordinates"])
                points.pop(closest.id)
                closest.id = pointData["name"]
                points[pointData["name"]] = closest

    return points