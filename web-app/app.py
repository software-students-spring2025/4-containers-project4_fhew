"""Flask web app to locate nearest emergency services for users."""

from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017")
db = client["emergency_services"]
#we will obv have to change this once the mongodb database is sest up

@app.route("/")
def home():
    """Render the homepage."""
    return render_template("home.html")

@app.route("/find-location", methods=["POST"])
def find_location():
    """Collect geolocationdata and store it in the mongodb database."""
    data = request.get_json()
    db.locations.insert_one(data)
    return {"message": "Location found"}

@app.route("/show-results")
def show_results():
    """Show results from the nearest emergency services search."""
    analysis = db.analysis.find_one(sort=[('_id', -1)])  # Get the latest result
    if analysis:
        services = analysis.get("nearby_stations", [])
        risk = analysis.get("risk_level", "Unknown")
        user_location = analysis.get("user_location")
        return render_template(
            "show_results.html",
            services=services,
            risk=risk,
            image_path="static/map.png"
        )
    else:
        return render_template("show_results.html", services=[], risk="No data", image_path=None)

@app.route("/mock-data")
def insert_mock_data():
    """Insert mock GPS + analysis data into MongoDB for testing visualization."""
    mock_result = {
        "user_location": {
            "latitude": 40.5412,
            "longitude": -74.1515,
        },
        "nearby_stations": [
            {
                "station_name": "Engine 161/Ladder 81",
                "latitude": 40.5416,
                "longitude": -74.1519,
                "functionalities": ["pumper", "ladder"],
                "distance_km": 0.05,
                "type": "Fire Station",
                "name": "Engine 161",
                "distance": 0.05,
                "travel_time": 1
            }
        ],
        "risk_level": "moderate risk"
    }
    db.analysis.insert_one(mock_result)

    # Generate map visualization
    from ml_client import visualize_stations
    visualize_stations(
        user_location=mock_result["user_location"],
        nearby_stations=mock_result["nearby_stations"],
        image_name="map.png",
        output_dir="/app/static"
    )
    return "✅ Mock data inserted and image generated."

@app.route("/map")
def show_map():
    """Display just the generated map image."""
    return render_template("map.html", image_path="static/map.png")

# main driver function
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=False, use_debugger=False)
    #won't let me access the site without the host and port params