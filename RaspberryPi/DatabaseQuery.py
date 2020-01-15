import pyrebase
import FirebaseConfig.Configure as firebase


# Reference to firebese databse
dbRef = firebase.dbRef

def getFreeVisitorSlot():
    freeSlots = dbRef.child("ParkingSlots").order_by_child(
        "Type").equal_to("Visitor").order_by_child("Allotted").equal_to(False).get()
    try:
        freeSlot = freeSlots[0]
        slotIndex = freeSlot.key()
        slotNumber = freeSlot.val()["SlotNo"]
        # Update database
        dbRef.child("ParkingSlots").child(slotIndex).update({"Allotted": True})
        return slotNumber
    except IndexError: # No free slots
        return ""


def verifyResident(licensePlateNumber):
    residents = dbRef.child("ResidentVehicles").order_by_child(
        "VehicleNo").equal_to(licensePlateNumber).get()
    try:
        allottedSlot = residents[0].val()["AllottedSlot"]
        return (True, allottedSlot)
    except IndexError: # Not a resident
        return (False, "")  


def verifyAndAllotVisitor(licensePlateNumber):
    visitors = dbRef.child("Visitors").order_by_child(
        "VehicleNo").equal_to(licensePlateNumber).get()
    try:
        visitor = visitors[0]
        visitorKey = visitor.key()
        updateInfo = {}
        updateInfo["Arrived"] = True
        allottedSlot = getFreeVisitorSlot() # Returns "" if no slots available
        updateInfo["AllottedSlot"] = allottedSlot
        # Update the visitor details
        dbRef.child("Visitors").child(visitorKey).update(updateInfo)
        return (True, allottedSlot)
    except IndexError: # Not a visitor
        return (False, "")

def deleteVisitor(licensePlateNumber):
    details = dbRef.child("Visitors").order_by_child("VehicleNo").equal_to(licensePlateNumber).get()
    try:
        key = details[0].key()
        slot = details[0].val()["AllottedSlot"]
        dbRef.child("Visitors").child(key).remove()
        freeSlot(slot)
    except IndexError: # Record not present in visitor table i.e., is a resident
        pass

def freeSlot(slot):
    slotDetails = dbRef.child("ParkingSlots").order_by_child("SlotNo").equal_to(slot).get()
    key = slotDetails[0].key()
    updateInfo = {"Allotted" : False}
    dbRef.child("ParkingSlots").child(key).update(updateInfo)

if __name__ == "__main__":
    print(verifyResident("KA09A1111"))
    print(verifyResident("KA09A1122"))
    print(verifyAndAllotVisitor(("KA47P0090")))
    print(verifyAndAllotVisitor(("KA05P9999")))
    print(getFreeVisitorSlot())
    freeSlot("V01")
    deleteVisitor("lol")
