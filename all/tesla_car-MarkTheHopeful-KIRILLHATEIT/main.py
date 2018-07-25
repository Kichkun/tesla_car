import math

MARGIN = 270


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):  
        return self.x * other.x + self.y * other.y

    def __mod__(self, other):  
        return self.x * other.y - self.y * other.x


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def makeVectorDir(pointStart, pointDir):
    return Vector(pointDir.x - pointStart.x, pointDir.y - pointStart.y)


def getAngle_point(x, y, x_to, y_to, vector_dir):  
    vector_move = Vector(x_to - x, y_to - y)  
    return (math.degrees(math.atan2(vector_dir * vector_move, vector_dir % vector_move)) + MARGIN) % 360  


def getAngle(pointStart, pointStop, pointDir):
    return getAngle_point(pointStart.x, pointStart.y, pointStop.x, pointStop.y, makeVectorDir(pointStart, pointDir))


print(getAngle(Point(0, 0), Point(2, 1), Point(1, 2)))
