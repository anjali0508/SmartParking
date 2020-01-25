import cv2
import RPi.GPIO as GPIO
import time
import DatabaseQuery as db
import PlateRecognizer as lpr
import PiFunctions as pi


# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
# Set up GPIO pins
residentRowPins = [3, 5]
residentColPins = [7, 11, 13]
visitorRowPins = [36,32]
visitorColPins = [31,33,35]
for pin in visitorRowPins:
    GPIO.setup(pin, GPIO.OUT)
for pin in visitorColPins:
    GPIO.setup(pin, GPIO.OUT)
for pin in residentRowPins:
    GPIO.setup(pin, GPIO.OUT)
for pin in residentColPins:
    GPIO.setup(pin, GPIO.OUT)
    
pi.setLEDGrid(residentRowPins, residentColPins)
pi.setLEDGrid(visitorRowPins, visitorColPins)
    
accessAllowedLED = 16
accessDeniedLED = 8
entryPirPin = 37
exitPirPin = 29
motorPin = 40
cameraPin = 18
slot=""

entryMotionFlag = False
exitMotionFlag = False
accessDenied = False

while True: 
    # Entry gate 
    motion, entryMotionFlag = pi.detectMotion(entryPirPin)
    if motion == True:
        accessDenied = True
        image = pi.getImage()
        plateNumber = lpr.extractLPN(image)
        print(plateNumber)
        # Verify from database
        # Verify resident
        verified, slot = db.verifyResident(plateNumber)
        if verified == True:
            accessDenied = False
            pi.operateLED(accessAllowedLED)
            pi.operateMotor(motorPin, "OPEN")
            # Guide to the slot
            pi.showPath(slot, residentRowPins, residentColPins)
            time.sleep(5)
            pi.operateMotor(motorPin, "CLOSE")
            pi.setLEDGrid(residentRowPins, residentColPins) # Reset LED grid

        # Verify visitor
        else:
            verified, slot = db.verifyAndAllotVisitor(plateNumber)
            if verified == True and slot != "":
                accessDenied = False
                pi.operateLED(accessAllowedLED) 
                pi.operateMotor(motorPin, "OPEN")
                pi.showPathVisitor(slot, visitorRowPins, visitorColPins)
                time.sleep(5)
                pi.operateMotor(motorPin, "CLOSE")
                pi.setLEDGrid(visitorRowPins, visitorColPins) # Reset LED grid

        if accessDenied == True:
            pi.operateLED(accessDeniedLED)
    
    # Exit gate
    motion, exitMotionFlag = pi.detectMotion(exitPirPin)
    if motion == True:
        plateNumber = lpr.extractLPN(imageName)
        db.deleteVisitor(plateNumber)
        









