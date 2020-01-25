import cv2 
import numpy as np
import pytesseract
from PIL import Image
import re

def show(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)

def preprocesing(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
    noiseless = cv2.subtract(gray, tophat)
    edges = cv2.Canny(noiseless, 100, 150)
    blur = cv2.GaussianBlur(edges, (5,5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 9)
    return thresh

def getSuitableContours(image, original):
    # INPUT: Pre-processed image [and original image for visualization]
    # OUTPUT: List of suitable contours
    height, width = image.shape
    # opencv v4
    contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Obtain large contours lying in the bottom half of the image
    largeContours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    bottomContours = list(filter(lambda contour : cv2.boundingRect(contour)[1] > height / 2, largeContours))
    
    # Visualization
    # original = original.copy()
    # cv2.drawContours(original, bottomContours, -1, (0,255,0), 2)
    #show("Suitable Contours", original)
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
        plate = image[y : y + h, x : x + w]
        #show("Plate", plate)

        # Convert to pillow Image format
        plate = Image.fromarray(plate)
        text = pytesseract.image_to_string(plate, lang="eng")
        plateNumber = getLPNumber(text)
        if plateNumber != False:
            print("The License Plate Number is", plateNumber)
            return plateNumber
        
    print("Failed to obtain License Plate Number")
    return ""

def getLPNumber(text):
    # INPUT: List of numbers obtained from all suitable contours
    # OUTPUT: Cleaned Registraion Number of the vehicle
    text = re.sub(r'[^\w]','',text)
    text = text.strip()
    if(text.isupper() or text.isdigit()):
        if (len(text)>5 and len(text)<=10):  
            print("Car number is:",text)
            return text
    return False

def extractLPN(image):   
    original = image
    # original = cv2.imread(imageName)
    # original = cv2.resize(original, (620, 480))
    preprocessed = preprocesing(original)
    suitableContours = getSuitableContours(preprocessed, original)
    rawNumbers = getRawLPNumbers(suitableContours, original)
    cleanNumber = getLPNumber(rawNumbers)
    # cv2.destroyAllWindows
    return cleanNumber

if __name__ == "__main__":

    resident = "Images/Car-resident.jpg"
    extractLPN(resident)
    visitor = "Images/Car-visitor.jpg"
    extractLPN(visitor)