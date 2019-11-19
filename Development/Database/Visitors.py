from firebase import firebase
import IDGenerator

firebase = firebase.FirebaseApplication(
    'https://smartparkingsystem-bca72.firebaseio.com/', None)
id = IDGenerator.ID()


class Visitor:
    def __init__(self, flatNo, vehicleNo, expectedTime,  name="", arrived=False, departed=False, allottedSlot=""):
        self.flatNo = flatNo
        self.vehicleNo = vehicleNo
        self.name = name
        self.expectedTime = expectedTime
        self.arrived = arrived
        self.departed = departed
        self.allottedSlot = allottedSlot

    def getJSONRep(self):
        json = {}
        json["FlatNo"] = self.flatNo
        json["VehicleNo"] = self.vehicleNo
        json["Name"] = self.name
        json["ExpectedTime"] = self.expectedTime
        json["Arrived"] = self.arrived
        json["Departed"] = self.departed
        json["AllottedSlot"] = self.allottedSlot
        return json


class Visitors:
    def __init__(self):
        pass

    def insert(self, visitor):
        visitorID = id.getNextVisitorID()
        data = visitor.getJSONRep()
        firebase.put("Visitors", visitorID, data)
        print("Inserted into database")

    def getAll(self):
        allVisitors = firebase.get("/", "Visitors")
        for visitor in allVisitors:
            print(visitor)
        return allVisitors


if __name__ == "__main__":
    visitors = Visitors()
    visitor = Visitor("101", "KA05P9999", "01/11/19 12:00")
    visitors.insert(visitor)
    visitor = Visitor("102", "KA09A2222", "01/11/19 12:00")
    visitors.insert(visitor)
    visitors.getAll()
