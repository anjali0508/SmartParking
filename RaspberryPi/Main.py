import cv2

import DatabaseQuery as db
import PlateRecognizer as lpr
import PiFunctions as pi

# Import GPIO library
# Set up GPIO pins 

imageIndex = 0 #A varable to help alternating between images supplied to pi
images = [] # Image names

while True:
    motion = pi.detectMotion(pirPin)
    if motion == "MotionStopped":
        pi.operateLED(cameraPin)

        # Load an image from memory and get plate number
        imageName = images[imageIndex]
        imageIndex = (imageIndex + 1) % len(images)
        plateNumber = lpr.extractLPN(imageName)

        # Verify from database
        # Verify resident
        verified, slot = db.verifyResident(plateNumber)
        if verified == True:
            pi.operateLED(accessAllowedLED)
            pi.operateMotor(motorPin, "OPEN")
            # Guide to the slot
            # ..
            # ..
            time.sleep(5)
            pi.operateMotor(motorPin, "CLOSE")

        # If not verify visitor
        verified, slot = db.verifyAndAllotVisitor(plateNumber)
        if verified == True and slot != "":
            pi.operateLED(accessAllowedLED) 
            pi.operateMotor(motorPin, "OPEN")
            # Guide to the slot
            # ..
            # ..
            time.sleep(5)
            pi.operateMotor(motorPin, "CLOSE")

        else:
            pi.operateLED(accessDeniedLED)









