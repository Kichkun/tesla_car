
import numpy as np
import cv2
import math
import RPi.GPIO as GPIO
from time import sleep
import sys

s = sys.stdin

class Moving:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(3, GPIO.OUT)
        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(40, GPIO.OUT)
        GPIO.setup(38, GPIO.OUT)
        self.p = GPIO.PWM(5, 255)
        self.p1 = GPIO.PWM(40, 255)
    def move_forward(self):
        print("f")
        GPIO.output(3, False)
        GPIO.output(38, True)
        self.p.start(100)
        self.p1.start(100)
        
    def rotate_left(self):
        print("l")
        GPIO.output(3, False)
        GPIO.output(38, False)
        self.p.start(100)
        self.p1.start(100)
        
    def rotate_right(self):
        print("r")
        GPIO.output(3, True)
        GPIO.output(38, True)
        self.p.start(100)
        self.p1.start(100)
        
    def stop(self):
        self.p.stop()
        self.p1.stop()
        GPIO.output(3, False)
        GPIO.output(38, False)
        

MARGIN = 270


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):  
        return self.x * other.x + self.y * other.y

    def __mod__(self, other):  
        return self.x * other.y - self.y * other.x

    def __len__(self):
        return math.sqrt(self.x * self.x + self.y * self.y)


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

move = Moving()
markers = [[265, 0], [0, 0], [265, 440], [0, 440], [265, 880], [0, 880],
           [265, 1320], [0, 1320], [265, 1760], [0, 1760], [265, 2200], [0, 2200],
           [795, 0], [530, 0], [795, 440], [530, 440], [795, 880], [530, 880],
           [795, 1320], [530, 1320], [795, 1760], [530, 1760], [795, 2200], [530, 2200]
           ] 
idm = 2

cap = cv2.VideoCapture(0)  
# dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
# dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
rotate = False
count = 0
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    height = len(frame)
    width = len(frame[0])
    l = 40.  
    center_x = width // 2  
    center_y = height // 2
    up_x = width // 2
    up_y = height
  
    gray_color = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgpoints = cv2.aruco.detectMarkers(gray_color, dictionary)
    if len(corners) == 0:
       count += 1
       if(count > 30): 
           move.stop()
           print(count)
        
    if len(corners) > 0:
        print(0)
        count  = 0
        x0, y0 = corners[0][0][0]
        x1, y1 = corners[0][0][3]
        # x2, y2 = x0 + l, y0
        x2, y2 = np.float32(x0 + l), y0
        vector_1_0 = Vector(x1 - x0, y1 - y0)
        vector_2_0 = Vector(x2 - x0, y2 - y0)
        scalar_mult = (x1 - x0) * (x2 - x0) + (y1 - y0) * (y2 - y0)
        vector_mult = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2) * math.sqrt((x2 - x0) ** 2 + (y2 - y0) ** 2)
        sin = vector_mult / length
        cos = scalar_mult / length
        center_y -= y0
        up_x -= x0
        up_y -= y0
        center_x1 = center_x * cos + center_y * sin
        center_y1 = -center_x * sin + center_y * cos
        up_x1 = up_x * cos + up_y * sin
        up_y1 = -up_x * sin + up_y * cos
        print(ids[0])
        if int(ids[0]) < len(markers):
            marker_x, marker_y = markers[int(ids[0])]
            center_x_absolute = center_x1 - marker_x
            center_y_absolute = center_y1 - marker_y
            up_x_absolute = up_x1 - marker_x
            up_y_absolute = up_y1 - marker_y
            angle = getAngle(Point(center_x_absolute, center_y_absolute), Point(markers[idm][0], markers[idm][1]), Point(up_x_absolute, up_y_absolute))
            if(not rotate and (10 <= angle and angle <= 350)):
                rotate = True
                if angle > 180:
                    move.rotate_left()
                else:
                    move.rotate_right()
            if(rotate and (10 >= angle or angle >= 350)):
                rotate = False
                move.move_forward()
            #print(angle)
        '''cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        cv2.line(frame, (x0, 0), (x0, height), (255, 0, 0))
        cv2.line(frame, (0, y0), (height, y0), (255, 0, 0))
        cv2.line(frame, (x0, y0), (x1, y1), (0, 0, 255))
        cv2.line(frame, (x0, y0), (x2, y2), (0, 0, 255))
    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()'''
