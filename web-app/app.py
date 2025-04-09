"""Flask web app to locate nearest emergency services for users."""

from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017")
db = client["emergency_services"]
#we will obv have to change this once the mongodb database is sest up

@app.route("/")
def home():
    """Render the homepage."""
    return render_template("home.html")

@app.route("/find-location", methods=["POST"])
def find_location(reqType):
    """Collect geolocationdata and store it in the mongodb database."""
    data = {}
    data.Timestamp = datetime.now()
    data.ReqType = reqType
    #data.location = ~~~ needs to still be found
    data.resultIDs = []
    db.Request.insert_one(data)
    return {"message": "Location found"}

@app.route("/show-results/<id>")
def show_results(id):
    """Show results from the nearest emergency services search."""
    # Get the latest result
    req = db.Request.find_one({'_id':id})
    nearby_services = []
    for resIds in req.resultIDs:
        nearby_services.append(db.Result.find_one({'_id':resIds}))
    if nearby_services.count > 0:
        #risk = analysis.get("risk_level", "Unknown") ~~Needs to be calculated~~
        user_location = req.location
        return render_template(
            "show_results.html",
            services=nearby_services,
            risk="Placeholder",
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
    #fixed port 5000 issue by changing to 5002