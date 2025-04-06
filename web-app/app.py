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
    nearby_services = list(db.results.find())
    #temp because I'm not sure how this will work with the ML model
    return render_template("show_results.html", services=nearby_services)

# main driver function
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True) 
    #won't let me access the site without the host and port params