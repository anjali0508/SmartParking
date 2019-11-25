import cv2

import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

import DatabaseQuery as db
import PlateRecognizer as lpr
import PiFunctions as pi

# Import GPIO library
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
    
pi.setGridResident(residentRowPins, residentColPins)
pi.setGridVisitor(visitorRowPins, visitorColPins)
    
accessAllowedLED = 16
accessDeniedLED = 8
entryPirPin = 37
exitPirPin = 29
motorPin = 40
cameraPin = 18
slot=""

imageName = "Images/car7.jpg"# Image names

while True:
    accessDenied = False
    motion = pi.detectMotion(entryPirPin)
    if motion == "motionstopped":
        accessDenied = True
        pi.operateLED(cameraPin)

        # Load an image from memory and get plate number
        plateNumber = lpr.extractLPN(imageName)
        print(plateNumber)
        # Verify from database
        # Verify resident
        verified, slot = db.verifyResident(plateNumber)
        if verified == True:
            accessDenied = False
            pi.operateLED(accessAllowedLED)
            pi.operateMotor(motorPin, "OPEN")
            # Guide to the slot
            pi.showPathResident(slot, residentRowPins, residentColPins)
            time.sleep(5)
            pi.operateMotor(motorPin, "CLOSE")
            print("done")
            pi.setGridResident(residentRowPins, residentColPins)

        # If not verify visitor
        else:
            verified, slot = db.verifyAndAllotVisitor(plateNumber)
            if verified == True and slot != "":
                accessDenied = False
                pi.operateLED(accessAllowedLED) 
                pi.operateMotor(motorPin, "OPEN")
                pi.showPathVisitor(slot, visitorRowPins, visitorColPins)
            # Guide to the slot
            # ..
            # ..
                time.sleep(2)
                pi.operateMotor(motorPin, "CLOSE")
                pi.setGridVisitor(visitorRowPins, visitorColPins)
            

        if accessDenied == True:
            pi.operateLED(accessDeniedLED)
    
    motion = pi.detectMotion(exitPirPin)
    if motion == "motionstopped":
        print("exit")
        plateNumber = lpr.extractLPN(imageName)
        print(plateNumber)
        db.deleteVisitor(plateNumber)
        









