import RPi.GPIO as GPIO
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

# Initialize camera 
camera = PiCamera()
camera.resolution = (640, 480)
cameraStream = PiRGBArray(camera)

def operateLED(LEDPin):
    GPIO.setup(LEDPin, GPIO.OUT)    
    GPIO.output(LEDPin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LEDPin, GPIO.LOW)

def setLEDGrid(rowPins, colPins):
    # Set the led pins to opposite polarity, so that they are OFF initially
    for rowPin in rowPins:
        GPIO.output(rowPin, GPIO.LOW)
    for colPin in colPins:
        GPIO.output(colPin, GPIO.HIGH)

def showPath(slot, rowPins, colPins):
    # Light up the path in LED matrix
    section, row, col = slot[0], int(slot[1]), int(slot[2])
    GPIO.output(rowPins[row], GPIO.HIGH)
    print(rowPins[row])
    print("Row lit", row)
    for i in range(col + 1):
        GPIO.output(colPins[i], GPIO.LOW)
        print(colPins[i])
        print("Column lit", i)

def operateMotor(servoPIN, mode):
    GPIO.setup(servoPIN, GPIO.OUT)
    #p.start(7.5) # Initialization
    print(mode)
    if(mode=="OPEN"):
        p = GPIO.PWM(40, 50)
        p.start(7.5)
        print("motor")
        try:
            p.ChangeDutyCycle(7.5)  # turn towards 0 degree
            time.sleep(1)
            p.ChangeDutyCycle(2.5)
        except KeyboardInterrupt:
            p.stop()
            GPIO.cleanup()
    elif(mode=="CLOSE"):
        p = GPIO.PWM(40, 50)
        p.start(2.5)
        print("motor")
        try:
            p.ChangeDutyCycle(2.5)  # turn towards 0 degree
            time.sleep(1)
            p.ChangeDutyCycle(7.5)
        except KeyboardInterrupt:
            p.stop()
            GPIO.cleanup()

def detectMotion(pirPin, motionFlag):
    pirState = GPIO.input(pirPin)
    if pirState == 0 and motionFlag == True:                 #When output from motion sensor is LOW
        motionFlag = False
        return True, motionFlag
    elif pirState == 1:                           #When output from motion sensor is HIGH
        print("Motion detected")
        motionFlag = True
    return False, motionFlag

def getImage():
    camera.capture(cameraStream, format="bgr")
    image = cameraStream.array
    return image