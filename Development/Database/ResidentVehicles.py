from firebase import firebase
import IDGenerator

firebase = firebase.FirebaseApplication(
    'https://smartparkingsystem-bca72.firebaseio.com/', None)
id = IDGenerator.ID()


class Resident:
    def __init__(self, flatNo, name, email="", phoneNo="", password=""):
        self.flatNo = flatNo
        self.name = name
        self.email = email
        self.phoneNo = phoneNo
        self.password = password

    def getJSONRep(self):
        json = {}
        json["FlatNo"] = self.flatNo
        json["Name"] = self.name
        json["Email"] = self.email
        json["PhoneNo"] = self.phoneNo
        json["Password"] = self.password
        return json


class Residents:
    def __init__(self):
        pass

    def insert(self, resident):
        residentID = id.getNextResidentID()
        data = resident.getJSONRep()
        firebase.put("Residents", residentID, data)
        print("Inserted into database")

    def getAll(self):
        allResidents = firebase.get("/", "Residents")
        for resident in allResidents:
            print(resident)


if __name__ == "__main__":
    resident = Resident(101, "Ananya")
    residents = Residents()
    residents.insert(resident)
    residents.getAll()
    resident = Resident(102, "Haha")
    residents.insert(resident)
    residents.getAll()
