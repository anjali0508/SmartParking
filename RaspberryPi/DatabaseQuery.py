import pyrebase
import FirebaseConfig.Configure as firebase

# Reference to firebese databse
dbRef = firebase.dbRef


def getFreeVisitorSlot():
    # Finds an empty slot for visitor parking
    # Input: Nil
    # Output: Slot Number if free slots are available, else ''

    freeSlots = dbRef.child("ParkingSlots").order_by_child(
        "Type").equal_to("Visitor").order_by_child("Allotted").equal_to(False).get()

    for freeSlot in freeSlots:
        slotIndex = freeSlot.key()
        slotNumber = freeSlot.val()["SlotNo"]
        # Update database
        dbRef.child("ParkingSlots").child(slotIndex).update({"Allotted": True})
        return slotNumber
    return ""


def verifyResident(licensePlateNumber):
    # Checks whether a given License Plate NUmber belongs to a resident
    # Input: License Plate Number
    # Output: if resident: (True, parking slot)
    #         else: (False, '')

    residentDetails = dbRef.child("ResidentVehicles").order_by_child(
        "VehicleNo").equal_to(licensePlateNumber).get()

    # This query returns a single resident if number exists. Obtain slot number and return
    # If the number doent exist in database, returned object is empty

    for resident in residentDetails:
        allottedSlot = resident.val()["AllottedSlot"]
        return (True, allottedSlot)
    return (False, "")


def verifyAndAllotVisitor(licensePlateNumber):
    # Checks whether a given License Plate NUmber belongs to a registered visitor
    # If true, allocates a parking slot
    # Input: License Plate Number
    # Output: if visitor registered:
    #             if free slot available: (True, parking slot)
    #             else: (True, '')
    #         else: (False, '')

    visitorDetails = dbRef.child("Visitors").order_by_child(
        "VehicleNo").equal_to(licensePlateNumber).get()

    for visitor in visitorDetails:
        visitorKey = visitor.key()
        updateInfo = {}
        updateInfo["Arrived"] = True
        allottedSlot = getFreeVisitorSlot()
        updateInfo["AllottedSlot"] = allottedSlot
        # Update the visitor details
        dbRef.child("Visitors").child(visitorKey).update(updateInfo)
        return (True, allottedSlot)
    return (False, "")


if __name__ == "__main__":
    print(verifyResident("KA09A1111"))
    # print(verifyResident("KA09A1122"))
    # print(verifyAndAllotVisitor(("KA09A2212")))
    # print(verifyAndAllotVisitor(("KA05P9999")))
    # print(verifyAndAllotVisitor(("KA09A2222")))
    # print(verifyAndAllotVisitor(("KA09A2212")))
