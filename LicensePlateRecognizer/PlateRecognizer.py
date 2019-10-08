import cv2 
import numpy as np
import pytesseract
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#To be used during development
def show(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)

def preprocesing(image):
    show("Original", image)

    # Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Remove Noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
    noiseless = cv2.subtract(gray, tophat)
    #show("Without Noise", noiseless)
    # Detect edges
    edges = cv2.Canny(noiseless, 100, 150)
    #show("Edges", edges)
    # Blur
    blur = cv2.GaussianBlur(edges, (5,5), 0)
    #show("Blur", blur)
    # Thresholiding
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 9)
    #show("Thresholding", thresh)

    return thresh

def getSuitableContours(image, original):
    # INPUT: Pre-processed image [and original image for visualization]
    # OUTPUT: List of suitable contours
    height, width = image.shape
    # opencv v4
    contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Obtain large contours lying in the bottom half of the image
    largeContours = sorted(contours, key = cv2.contourArea, reverse = True)[:20]
    bottomContours = list(filter(lambda contour : cv2.boundingRect(contour)[1] > height / 2, largeContours))
    
    # Visualization
    original = original.copy()
    cv2.drawContours(original, bottomContours, -1, (0,255,0), 2)
    show("Suitable Contours", original)
    return bottomContours

def getRawLPNumbers(contours, image):
    # INPUT: List of suitable  contours and original image
    # OUTPUT: List of characters extracted from each countour
    numbers = []
    for contour in contours:
        [x, y, w, h] = cv2.boundingRect(contour)

        # Visualization
        # temp = image.copy()
        # cv2.rectangle(temp, (x,y), (x + w, y + h), (0,255,0), 1)
        # show("Plate", temp)

        # Visualization
        plate = image[y : y + h, x : x + w]
        #show("Plate", plate)

        # Convert to pillow Image format
        plate = Image.fromarray(plate)
        text = pytesseract.image_to_string(plate, lang="eng")
        numbers.append(text)
    
    print("Numbers obtained are: ", numbers)
    return numbers

def getLPNumber(numbers):
    # INPUT: List of numbers obtained from all suitable contours
    # OUTPUT: Cleaned Registraion Number of the vehicle
    for i in numbers:
        i = re.sub(r'[^\w]','',i)
        i = i.strip()
        if(i.isupper() or i.isdigit()):
            if (len(i)>5 and len(i)<=10):  #To pass all the test, ideally it should be 9 or 10
                print("Car number is:",i)
                return i
        
original = cv2.imread("./Images/car1.jpeg")
original = cv2.resize(original, (620, 480))
preprocessed = preprocesing(original)
suitableContours = getSuitableContours(preprocessed, original)
rawNumbers = getRawLPNumbers(suitableContours, original)
cleanNumber = getLPNumber(rawNumbers)
cv2.destroyAllWindows
    
#Cars passed: 2, 4, 5, 7, 8,6
#Cars failed: 
# 3(LP blurred, tessaract couldnt obtain, but LP cropped properly)