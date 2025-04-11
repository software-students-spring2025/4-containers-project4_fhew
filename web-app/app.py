"""Flask web app to locate nearest emergency services for users."""

from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import os
import requests

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017")
db = client["emergency_services"]


@app.route("/")
def home():
    """Render the homepage."""
    return render_template("home.html")


@app.route("/find-location", methods=["POST"])
def find_location():
    """Collect geolocation data and store it in the mongodb database."""
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

    ml_client_url = os.getenv("ML_CLIENT_URL", "http://ml-client:8000")
    requests.post(f"{ml_client_url}/analyze", json={"id": str(inserted.inserted_id)})
    return {"message": "Location saved", "id": str(inserted.inserted_id)}


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

    nearby_services.sort(key=lambda x: int(x["travel_time"]))

    user_location = req.get(
        "location", {"latitude": 0, "longitude": 0}
    )  # fallback if missing
    return render_template(
        "show_results.html",
        services=nearby_services,
        risk=req["risk"],
        image_path="static/map.png",
        user_location=user_location,
        id=id,
    )


@app.route("/map/<id>")
def show_map(id):
    """Display just the generated map image."""
    req = db.Request.find_one({"_id": ObjectId(id)})
    nearby_services = []
    for res_id in req["resultIDs"]:
        result = db.Result.find_one({"_id": res_id})
        if result:
            nearby_services.append(result)

    nearby_services.sort(key=lambda x: int(x["travel_time"]))

    return render_template(
        "map.html", services=nearby_services, image_path="static/map.png"
    )


# main driver function
if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=5002, debug=True, use_reloader=False, use_debugger=False
    )
    # fixed port 5000 issue by changing to 5002
