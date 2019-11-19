from flask import Flask, make_response, jsonify, abort
import pyrebase
import FirebaseConfig.Configure as firebase

# Reference to firebese databse
dbRef = firebase.dbRef

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/")
def index():
    return "Hello World"


@app.route("/Resident/<int:id>/Profile", methods=["GET"])
def getResident(id):
    residentDetails = dbRef.child("Residents").order_by_child(
        "FlatNo").equal_to(id).get()
    # This query returns a single resident if present.
    for resident in residentDetails:
        return jsonify({"Resident": resident.val()})
    # Else throw 404 error
    abort(404)


@app.route("/Resident/<int:id>/home", methods=["GET"])
def home(id):
    id = str(id)
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


if __name__ == '__main__':
    app.run(debug=True)
