from firebase import firebase
import IDGenerator

firebase = firebase.FirebaseApplication(
    'https://smartparkingsystem-bca72.firebaseio.com/', None)
id = IDGenerator.ID()


class ResidentVehicle:
    def __init__(self, flatNo, vehicleNo, allottedSlot):
        self.flatNo = flatNo
        self.vehicleNo = vehicleNo
        self.allottedSlot = allottedSlot

    def getJSONRep(self):
        json = {}
        json["FlatNo"] = self.flatNo
        json["VehicleNo"] = self.vehicleNo
        json["AllottedSlot"] = self.allottedSlot
        return json


class ResidentVehicles:
    def __init__(self):
        pass

    def insert(self, vehicle):
        vehicleID = id.getNextResidentVehicleID()
        data = vehicle.getJSONRep()
        firebase.put("ResidentVehicles", vehicleID, data)
        print("Inserted into database")

    def getAll(self):
        allVehicles = firebase.get("/", "ResidentVehicles")
        for vehicle in allVehicles:
            print(vehicle)
        return allVehicles


if __name__ == "__main__":
    residentVehicles = ResidentVehicles()
    vehicle = ResidentVehicle("101", "KA05P9090", "R1")
    residentVehicles.insert(vehicle)
    vehicle = ResidentVehicle("102", "KA09A1111", "R2")
    residentVehicles.insert(vehicle)
    vehicle = ResidentVehicle("101", "KA10D1212", "R3")
    residentVehicles.insert(vehicle)
    residentVehicles.getAll()
