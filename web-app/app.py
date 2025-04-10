"""Flask web app to locate nearest emergency services for users."""

from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017")
db = client["emergency_services"]
# we will obv have to change this once the mongodb database is sest up


@app.route("/")
def home():
    """Render the homepage."""
    return render_template("home.html")


@app.route("/find-location", methods=["POST"])
def find_location():
    """Collect geolocationdata and store it in the mongodb database."""
    content = request.get_json()
    latitude = content.get("lat")
    longitude = content.get("long")
    if latitude is None or longitude is None:
        return {"error": "Missing coordinates"}, 400

    data = {
        "Timestamp": datetime.now(),
        "ReqType": "location_capture",
        "location": {"latitude": latitude, "longitude": longitude},
        "resultIDs": [],
    }

    inserted = db.Request.insert_one(data)
    return {"message": "Location saved", "id": str(inserted.inserted_id)}
    """
    data = {}
    data.Timestamp = datetime.now()
    data.ReqType = reqType
    #data.location = ~~~ needs to still be found
    data.resultIDs = []
    db.Request.insert_one(data)
    return {"message": "Location found"}
    """


@app.route("/show-results/<id>")
def show_results(id):
    """Show results from the nearest emergency services search."""
    # Get the latest result
    req = db.Request.find_one({"_id": ObjectId(id)})
    nearby_services = []
    for res_id in req["resultIDs"]:
        result = db.Result.find_one({"_id": res_id})
        if result:
            nearby_services.append(result)

    user_location = req.get(
        "location", {"latitude": 0, "longitude": 0}
    )  # fallback if missing
    return render_template(
        "show_results.html",
        services=nearby_services,
        risk="Placeholder",
        image_path="static/map.png",
        user_location=user_location,
    )
    # for resIds in req.resultIDs:
    # nearby_services.append(db.Result.find_one({'_id':resIds}))
    # if nearby_services.count > 0:
    # risk = analysis.get("risk_level", "Unknown") ~~Needs to be calculated~~
    # user_location = req.location
    # return render_template(
    # "show_results.html",
    # services=nearby_services,
    # risk="Placeholder",
    # image_path="static/map.png",
    # user_location = user_location
    # )
    # else:
    # return render_template("show_results.html", services=[], risk="No data", image_path=None)


@app.route("/map")
def show_map():
    """Display just the generated map image."""
    return render_template("map.html", image_path="static/map.png")


# main driver function
if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=5002, debug=True, use_reloader=False, use_debugger=False
    )
    # fixed port 5000 issue by changing to 5002
