import pyrebase
from . import ConfigDetails

firebase = pyrebase.initialize_app(ConfigDetails.config)
auth = firebase.auth()

email = ConfigDetails.email
password = ConfigDetails.password

user = auth.sign_in_with_email_and_password(email, password)
# userID = user["idToken"]
dbRef = firebase.database()

print("Firebase connection established")
