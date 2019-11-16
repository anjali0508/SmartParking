import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering


def operateLED(LEDPin):
    # Since we do not use an actual camera for this prototype, we replicate its operation using an led
    GPIO.output(LEDPin, GPIO.HIGH)
    sleep(1)
    GPIO.output(LEDPin, GPIO.LOW)

def setGrid(rowPins, colPins):
    # Set the led pins to opposite polarity, so that they are OFF initially
    for rowPin in rowPins:
        GPIO.output(rowPin, GPIO.LOW)
    for colPin in colPins:
        GPIO.output(colPin, GPIO.HIGH)

def showPath(slot, rowPins, colPins):
    section, row, col = slot[0], slot[1], slot[2]
    GPIO.output(rowPins[row], GPIO.HIGH)
    for i in range(col + 1):
        GPIO.output(colPins[i], GPIO.HIGH)

def operateMotor(servoPIN):
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
    p.start(2.5) # Initialization
    try:
        
        p.ChangeDutyCycle(2.5)  # turn towards 0 degree
        time.sleep(7) # sleep 1 second
        p.ChangeDutyCycle(12.5) # turn towards 180 degree
        time.sleep(1) # sleep 1 second 
        p.stop()
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
    # Mode can be "OPEN" or "CLOSE"
    #if mode == "OPEN":
        # Rotate 180
    #if mode == "CLOSE":
        # Rotate the other 180

def detectMotion(pirPin):
    # if motion detected and body stops moving, return motion stopped
    # return motion started
    # return no motion
    flag = 0
    GPIO.setup(pirPin, GPIO.IN)              
    GPIO.setup(3, GPIO.OUT)  
    while True:
        i=GPIO.input(pirPin)
        if i==0 and flag==1:                 #When output from motion sensor is LOW
            GPIO.output(3, 0)                #Turn OFF LED
            return "motion stopped"
        elif i==1:                           #When output from motion sensor is HIGH
            print("Intruder detected",i)
            flag = 1
            GPIO.output(3, 1)                #Turn ON LED
        time.sleep(1)
if (detectMotion(11))=="motion stopped":
    operateMotor(7)

    
