from firebase import firebase
import IDGenerator

firebase = firebase.FirebaseApplication(
    'https://smartparkingsystem-bca72.firebaseio.com/', None)
id = IDGenerator.ID()


class ParkingSlot:
    def __init__(self, slotNo, type, allotted=False):
        self.slotNo = slotNo
        self.type = type
        self.allotted = allotted

    def getJSONRep(self):
        json = {}
        json["SlotNo"] = self.slotNo
        json["Type"] = self.type
        json["Allotted"] = self.allotted
        return json


class ParkingSlots:
    def __init__(self):
        pass

    def insert(self, parkingSlot):
        slotID = id.getNextParkingSlotID()
        data = parkingSlot.getJSONRep()
        firebase.put("ParkingSlots", slotID, data)
        print("Inserted into database")

    def getAll(self):
        allSlots = firebase.get("/", "ParkingSlots")
        for slot in allSlots:
            print(slot)
        return allSlots


if __name__ == "__main__":
    parkingSlots = ParkingSlots()
    parkingSlot = ParkingSlot("R1", "Resident", True)
    parkingSlots.insert(parkingSlot)
    parkingSlot = ParkingSlot("R2", "Resident", True)
    parkingSlots.insert(parkingSlot)
    parkingSlot = ParkingSlot("R3", "Resident", True)
    parkingSlots.insert(parkingSlot)
    parkingSlot = ParkingSlot("V1", "Visitor")
    parkingSlots.insert(parkingSlot)
    parkingSlot = ParkingSlot("V2", "Visitor")
    parkingSlots.insert(parkingSlot)
    parkingSlots.getAll()
