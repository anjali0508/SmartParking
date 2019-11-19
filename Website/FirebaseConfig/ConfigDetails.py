import os

scriptDirectory = os.path.dirname(__file__)
serviceAccountDetails = os.path.join(
    scriptDirectory, "ServiceAccountDetails.json")

config = {
    "apiKey": "AIzaSyBCIN4n1oUa0KONFQykV5plcglIf3ZCSEY",
    "authDomain": "smartparkingsystem-bca72.firebaseapp.com",
    "databaseURL": "https://smartparkingsystem-bca72.firebaseio.com/",
    "storageBucket": "smartparkingsystem-bca72.appspot.com",
    "serviceAccount": serviceAccountDetails
}
email = "smartparking58@gmail.com"
password = "Smart@58"
