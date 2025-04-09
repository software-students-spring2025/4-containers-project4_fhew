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

@app.route("/map")
def show_map():
    """Display just the generated map image."""
    return render_template("map.html", image_path="static/map.png")

# main driver function
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=False, use_debugger=False)
    #won't let me access the site without the host and port params