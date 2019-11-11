import RPi.GPIO as GPIO 
from time import sleep
# GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering


def operateLED(LEDPin):
    # Since we do not use an actual camerap for this prototype, we replicate its operation using an led
    GPIO.output(LEDPin, GPIO.HIGH)
    sleep(1)
    GPIO.output(LEDPin, GPIO.LOW)

def operateMotor(motorPin, mode):
    # Mode can be "OPEN" or "CLOSE"
    if mode == "OPEN":
        # Rotate 180
    if mode == "CLOSE":
        # Rotate the other 180

def detectMotion(pirPin):
    # if motion detected and body stops moving, return motion stopped
    # return motion started
    # return no motion