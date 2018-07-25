import RPi.GPIO as GPIO
from time import sleep



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
        GPIO.output(3, False)
        GPIO.output(38,True )
        self.p.start(100)
        self.p1.start(100)
        
    def rotate_left(self):
        GPIO.output(3, False)
        GPIO.output(38, False)
        self.p.start(100)
        self.p1.start(100)
        
    def rotate_right(self):
        GPIO.output(3, True)
        GPIO.output(38, True)
        self.p.start(100)
        self.p1.start(100)
        
    def stop(self):
        self.p.stop()
        self.p1.stop()
        GPIO.output(3, False)
        GPIO.output(38, False)
        



