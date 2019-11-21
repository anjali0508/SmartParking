from flask import Flask, make_response, jsonify, abort, request
import pyrebase
import FirebaseConfig.Configure as firebase

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

# Change id to string
@app.route("/Resident/<int:id>/Profile", methods=["GET"])
def getResident(id):
    residentDetails = dbRef.child("Residents").order_by_child(
        "FlatNo").equal_to(id).get()
    # This query returns a single resident if present.
    for resident in residentDetails:
        return jsonify({"Resident": resident.val()})
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
    return jsonify({"Vehicles": vehicles, "VisitoVehicles": visitors})


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
    return jsonify({"Success": True}, 201)


@app.route("/Resident/<string:id>/DeleteVisitor", methods=["POST"])
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
    return jsonify({"Success": False, "Message": "Invalid Vehicle Number"}, 201)

# Change id to string
@app.route("/Resident/<int:id>/ChangePassword", methods=["POST"])
def changePassword(id):
    if not request.json or not "Password" in request.json:
        abort(400)
    # Hash later
    password = request.json["Password"]
    details = dbRef.child("Residents").order_by_child(
        "FlatNo").equal_to(id).get()
    for x in details:
        ID = x.key()
    dbRef.child("Residents").child(ID).update({"Password": password})
    return jsonify({"Success": True}, 201)


if __name__ == '__main__':
    app.run(debug=True)
