import cv2

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
    
setGridResident(residentRowPins, residentColPins)
setGridVisitor(visitorRowPins, visitorColPins)
    
cameraPin = accessDeniedLED = 38
accessAllowedLED = 38
pirPin = 37
motorPin = 40

imageIndex = 0 #A varable to help alternating between images supplied to pi
images = ["car7.jpg"] # Image names

while True:
    motion = pi.detectMotion(pirPin)
    if motion == "motionstopped":
        pi.operateLED(cameraPin)

        # Load an image from memory and get plate number
        imageName = images[imageIndex]
        imageIndex = (imageIndex + 1) % len(images)
        plateNumber = lpr.extractLPN(imageName)
        print(plateNumber)
        # Verify from database
        # Verify resident
        verified, slot = db.verifyResident(plateNumber)
        if verified == True:
            pi.operateLED(accessAllowedLED)
            pi.operateMotor(motorPin, "OPEN")
            # Guide to the slot
            showPathResident(slot, residentRowPins, residentColPins)
            time.sleep(5)
            pi.operateMotor(motorPin, "CLOSE")

        # If not verify visitor
        verified, slot = db.verifyAndAllotVisitor(plateNumber)
        if verified == True and slot != "":
            pi.operateLED(accessAllowedLED) 
            pi.operateMotor(motorPin, "OPEN")
            showPathResident(slot, visitorRowPins, visitorColPins)
            # Guide to the slot
            # ..
            # ..
            time.sleep(5)
            pi.operateMotor(motorPin, "CLOSE")

        else:
            pi.operateLED(accessDeniedLED)









