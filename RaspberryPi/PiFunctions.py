import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

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

def operateLED(LEDPin):
    # Since we do not use an actual camera for this prototype, we replicate its operation using an led
    GPIO.setup(LEDPin, GPIO.OUT)    
    GPIO.output(LEDPin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LEDPin, GPIO.LOW)

def setGridResident(rowPins, colPins):
    # Set the led pins to opposite polarity, so that they are OFF initially
    for rowPin in rowPins:
        GPIO.output(rowPin, GPIO.LOW)
    for colPin in colPins:
        GPIO.output(colPin, GPIO.HIGH)

def showPathResident(slot, rowPins, colPins):
    section, row, col = slot[0], int(slot[1]), int(slot[2])
    GPIO.output(rowPins[row], GPIO.HIGH)
    print(rowPins[row])
    print("Row lit", row)
    for i in range(col + 1):
        GPIO.output(colPins[i], GPIO.LOW)
        print(colPins[i])
        print("COl lit", i)

def setGridVisitor(rowPins, colPins):
    # Set the led pins to opposite polarity, so that they are OFF initially
    for rowPin in rowPins:
        GPIO.output(rowPin, GPIO.LOW)
    for colPin in colPins:
        GPIO.output(colPin, GPIO.HIGH)

def showPathVisitor(slot, rowPins, colPins):
    section, row, col = slot[0], int(slot[1]), int(slot[2])
    GPIO.output(rowPins[row], GPIO.HIGH)
    print(rowPins[row])
    print("Row lit", row)
    for i in range(col + 1):
        GPIO.output(colPins[i], GPIO.LOW)
        print(colPins[i])
        print("COl lit", i)



def operateMotor(servoPIN, mode):
    GPIO.setup(servoPIN, GPIO.OUT)
    
    p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
    p.start(7.5) # Initialization
    
    if(mode=="OPEN"):
        try:
            p.ChangeDutyCycle(2.5)  # turn towards 0 degree
        except KeyboardInterrupt:
            p.stop()
            GPIO.cleanup()
    else if(mode=="CLOSED"):
        try:
            p.ChangeDutyCycle(7.5) # turn towards 90 degree
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
    flag = 0
    motionLED = 38
    GPIO.setup(pirPin, GPIO.IN)              
    GPIO.setup(motionLED, GPIO.OUT)  
    while True:
        i=GPIO.input(pirPin)
        if i==0 and flag==1:                 #When output from motion sensor is LOW
            GPIO.output(motionLED, 0)                #Turn OFF LED
            operateMotor(40)
            return "motionstopped"
        elif i==1:                           #When output from motion sensor is HIGH
            print("Intruder detected",i)
            flag = 1
            GPIO.output(motionLED, 1)        #Turn ON LED
        time.sleep(1)

x = detectMotion(37)
if(x=="motionstopped"):
    setGridResident(residentRowPins, residentColPins)
    setGridVisitor(visitorRowPins, visitorColPins)
    slot = "R12"  #row column
    showPathVisitor(slot, visitorRowPins, visitorColPins)
