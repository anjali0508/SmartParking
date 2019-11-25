from flask import Flask, make_response, jsonify, abort, request, render_template, url_for, redirect, session
import pyrebase
import FirebaseConfig.Configure as firebase
import time
from Database.IDGenerator import ID as IDgen
IDgen = IDgen()
IDgen.setVisitorID()
IDgen.setResidentVehicleID()
IDgen.setResidentID()
IDgen.setParkingSlotID()

# Reference to firebese databse
dbRef = firebase.dbRef

app = Flask(__name__)


@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def badRequest(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route("/")
def index():
    return "Hello World"


@app.route("/login", methods=["POST"])
def login():
    if not request.json or not "Username" in request.json or not "Password" in request.json:
        abort(400)
    username = request.json["Username"]
    password = request.json["Password"]
    user = dbRef.chils("Residents").order_by_child(
        "FlatNo").equal_to(username).get()
    try:
        passwordCheck = user[0].val()["Password"]
        if password == passwordCheck:
            session["LoggedIn"] = True
            session["User"] = username
            return jsonify({"Login": "Successful"})
        else:
            return jsonify({"Login": "no"})
    except:
        return jsonify({"Login": "no"})

# Change id to string
@app.route("/Resident/<int:id>/Profile", methods=["GET"])
def getResident(id):
    residentDetails = dbRef.child("Residents").order_by_child(
        "FlatNo").equal_to(id).get()
    # This query returns a single resident if present.
    for resident in residentDetails:
        return render_template("ResidentProfile.html", details=resident.val(), id=str(id))
        # return jsonify({"Resident": resident.val()})
    # Else throw 404 error
    abort(404)


@app.route("/Resident/<string:id>/home", methods=["GET"])
def home(id):
    # id = str(id)
    # Get vehicle details
    vehicles = []
    vehicleDetails = dbRef.child("ResidentVehicles").order_by_child(
        "FlatNo").equal_to(id).get()
    for vehicle in vehicleDetails:
        details = vehicle.val()
        del details["FlatNo"]
        vehicles.append(details)
    # Get visitor details
    visitors = []
    visitorDetails = dbRef.child("Visitors").order_by_child(
        "FlatNo").equal_to(id).get()
    for visitor in visitorDetails:
        details = visitor.val()
        del details["FlatNo"]
        visitors.append(details)
    return render_template(
        "ResidentHome.html",
        vehicles=vehicles,
        vehicleCount=len(vehicles),
        visitorVehicles=visitors,
        visitorCount=len(visitors),
        id=id
    )
    # return jsonify({
    #     "Vehicles": vehicles,
    #     "VehicleCount": len(vehicles),
    #     "Visitors": visitors,
    #     "VisitorCount": len(visitors)})


@app.route("/Resident/<string:id>/AddVisitor", methods=["POST"])
def addVisitor(id):
    if not request.json or not "VehicleNo" in request.json:
        abort(400)
    visitor = {
        "AllottedSlot": "",
        "Arrived": False,
        "Departed": False,
        "FlatNo": id,
        "Name": request.json.get("Name", ""),
        "VehicleNo": request.json["VehicleNo"]
    }

    visitorID = IDgen.getNextVisitorID()
    dbRef.child("Visitors").child(visitorID).set(visitor)
    # Add a success message
    return jsonify({"Success": True}, 201)


@app.route("/Resident/<string:id>/DeleteVisitor", methods=["DELETE"])
def deleteVisitor(id):
    if not request.json or not "VehicleNo" in request.json:
        abort(400)
    vehicleNo = request.json["VehicleNo"]
    details = dbRef.child("Visitors").order_by_child(
        "VehicleNo").equal_to(vehicleNo).get()
    for x in details:
        visitorID = x.key()
        flatNo = x.val()["FlatNo"]
        break
    if flatNo == id:
        dbRef.child("Visitors").child(visitorID).remove()
        return jsonify({"Success": True}, 201)
        # send back 200
    return jsonify({"Success": False, "Message": "Invalid Vehicle Number"}, 201)

# Change id to string
@app.route("/Resident/<int:id>/ChangePassword", methods=["PUT"])
# ADD ENCRYPTION
# Method must be PATCH
def changePassword(id):
    if not request.json or not "CurrentPassword" in request.json or not "NewPassword" in request.json:
        abort(400)
    # Hash later
    currentPassword = request.json["CurrentPassword"]
    newPassword = request.json["NewPassword"]
    details = dbRef.child("Residents").order_by_child(
        "FlatNo").equal_to(id).get()
    for x in details:
        ID = x.key()
        password = x.val()["Password"]
        break
    if password == currentPassword:
        dbRef.child("Residents").child(ID).update({"Password": newPassword})
        return jsonify({"Success": True}, 201)
    else:
        return jsonify({"Success": False, "Message": "Password you entered is wrong"}, 201)


@app.route("/Admin/Residents", methods=["GET", "PUT", "DELETE", "POST"])
def residentFuctions():
    if request.method == "GET":
        residents = dbRef.child("Residents").get()
        details = [resident.val()
                   for resident in residents if resident.val() != None]
        # return jsonify({"Residents": details, "residentCount": len(details)}, 200)
        return render_template(
            "Admin_Residents.html",
            Residents=details,
            residentCount=len(details)
        )

    elif request.method == "POST":
        if not request.json or not "FlatNo" in request.json or not "Password" in request.json:
            print("lala")
            abort(400)
        resident = {
            "Email": request.json.get("Email", ""),
            "FlatNo": request.json["FlatNo"],
            "Name": request.json.get("Name", ""),
            "Password": request.json["Password"],
            "PhoneNo": request.json.get("PhoneNo", "")
        }
        residentID = IDgen.getNextResidentID()
        dbRef.child("Residents").child(residentID).set(resident)
        return jsonify({"Success": True}, 201)

    elif request.method == "PUT":
        if not request.json or not "FlatNo" in request.json:
            abort(400)
        resident = {}
        flatNo = request.json["FlatNo"]
        if "Name" in request.json:
            resident["Name"] = request.json["Name"]
        if "Email" in request.json:
            resident["Email"] = request.json["Email"]
        if "Password" in request.json:
            resident["Password"] = request.json["Password"]
        if "PhoneNo" in request.json:
            resident["PhoneNo"] = request.json["PhoneNo"]
        details = dbRef.child("Residents").order_by_child(
            "FlatNo").equal_to(flatNo).get()
        try:
            ID = details[0].key()
            dbRef.child("Residents").child(ID).update(resident)
            return jsonify({"Success": True}, 200)
        except:
            return jsonify({"Success": False, "Message": "Flat Number does not exist"})

    elif request.method == "DELETE":
        if not request.json or not "FlatNo" in request.json:
            abort(400)
        flatNo = request.json["FlatNo"]
        details = dbRef.child("Residents").order_by_child(
            "FlatNo").equal_to(flatNo).get()
        try:
            ID = details[0].key()
            if ID == None:
                return jsonify({"Success": False, "Message": "Flat Number does not exist"}, 404)
            dbRef.child("Residents").child(ID).remove()
            return jsonify({"Success": True}, 200)
        except IndexError:
            return jsonify({"Success": False, "Message": "Flat Number does not exist"}, 404)
        # DELETE VEHICLES TOO
    else:
        abort(404)


@app.route("/Admin/ResidentVehicles", methods=["GET", "DELETE", "POST"])
def residentVehicleFuctions():
    if request.method == "GET":
        vehicles = dbRef.child(
            "ResidentVehicles").get()
        details = [vehicles.val()
                   for vehicles in vehicles if vehicles.val() != None]
        # return jsonify({"Vehicles": details, "VehicleCount": len(details)}, 200)
        return render_template(
            "Admin_ResidentVehicles.html",
            vehicles=details,
            vehicleCount=len(details)
        )

    elif request.method == "POST":
        if (
            not request.json or
            not "FlatNo" in request.json or
            not "VehicleNo" in request.json or
            not "AllottedSlot" in request.json
        ):
            abort(400)

        slot = request.json["AllottedSlot"]
        slotDetails = dbRef.child("ParkingSlots").order_by_child(
            "SlotNo").equal_to(slot).get()
        try:
            if slotDetails[0].val()["Allotted"] == False:
                key = slotDetails[0].key()
                # Update slot details
                dbRef.child("ParkingSlots").child(
                    key).update({"Allotted": True})
                # Add vehicle
                vehicle = {
                    "FlatNo": request.json["FlatNo"],
                    "VehicleNo": request.json["VehicleNo"],
                    "AllottedSlot": request.json["AllottedSlot"]
                }
                vehicleID = IDgen.getNextResidentVehicleID()
                dbRef.child("ResidentVehicles").child(
                    vehicleID).set(vehicle)
                return jsonify({"Success": True})
            else:
                return jsonify({"Success": False, "Message": "Slot not free"})
        except IndexError:
            return jsonify({"Success": False, "Message": "Slot not available"})

    elif request.method == "DELETE":
        if not request.json or not "VehicleNo" in request.json:
            abort(400)
        vehicleNo = request.json["VehicleNo"]
        details = dbRef.child("ResidentVehicles").order_by_child(
            "VehicleNo").equal_to(vehicleNo).get()

        try:
            ID = details[0].key()
            if ID == None:
                return jsonify({"Success": False, "Message": "Vehicle does not exist"})
            slot = details[0].val()["AllottedSlot"]
            # Free the allotted slot
            slotDetails = dbRef.child("ParkingSlots").order_by_child(
                "SlotNo").equal_to(slot).get()
            key = slotDetails[0].key()
            dbRef.child("ParkingSlots").child(key).update({"Allotted": False})
            dbRef.child("ResidentVehicles").child(ID).remove()
            return jsonify({"Success": True})
        except IndexError:
            return jsonify({"Success": False, "Message": "Vehicle does not exist"})

    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
