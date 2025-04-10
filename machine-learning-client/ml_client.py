"""
ML client that analyzes data and stores results in MongoDB.

NYC Fire Station Data: https://data.gis.ny.gov/datasets/sharegisny::firestations/about

Note: The code must follow PEP 8, using Black for formatting and Pylint for linting.
"""

import os
import math
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
from config import GOOGLE_MAPS_API_KEY
import utm

app = Flask(__name__)

# Connect to MongoDB service in Docker
client = MongoClient("mongodb://mongodb:27017")
db = client["emergency_services"]
reqDB = db["Request"]  # DB of user input
resDB = db["Result"]  # DB of stored analysis


# Import CSV
CSV_PATH = "firestations_info.csv"
RISK_THRESHOLDS_KM = [1, 5, 10]  # these are cutoffs for risks


# analysis is invoked by the interface of the web app part
def run_analysis(reqID):
    
    """Main function for ML analysis."""
    req = reqDB.find_one({"_id":reqID})
    stations = load_station_data(CSV_PATH)
    nearby_stations = find_near_by_stations(
        req.get("location")["latitude"], req.get("location")["longitude"], stations
    )
    IDArray = []
    for station in nearby_stations:
        risk_level = assign_risk_level(nearby_stations)
        res = {
            "name" : station["Station Name"],
            "location" : {"longitude": station["longitude"], "latitude" : station["latitude"]},
            "address" : station["Address"],
            "travel_distance" : station["distance_km"] 
            #travel time
            #urgency
        }
        retID = resDB.insert_one(res).inserted_id
        IDArray.append(retID)

    reqDB.update_one({"_id":reqID},{"$set" : {"resultIDs":IDArray}})
    print("Analysis complete. Data inserted into MongoDB!")
    return reqID


def UTMtoLatLong(easting,northing):
    Lat, Long = utm.to_latlon(easting,northing,18,'T')
    return Lat,Long


def find_near_by_stations(user_lat, user_lon, stations, radius_km=5):
    """Find the nearest fire station."""
    nearby = []
    for station in stations:
        stationLat,stationLong = UTMtoLatLong(station["x"],station["y"])
        distance = haversine_distance(
            user_lat, user_lon, stationLat, stationLong
        )
        if distance <= radius_km:
            station_data = station.copy()
            station_data["distance_km"] = distance
            station_data["longitude"] = stationLong
            station_data["latitude"] = stationLat
            nearby.append(station_data)
    # Sort by distance, closest first.
    return sorted(nearby, key=lambda s: s["distance_km"])


# assign risk level based on the analysis
# low risk - surrounded by stations with all functionality
# moderate risk - surrounded by stations with two functions
# high risk - surrounded by a single with one function
# extremly hish risk - no fire station near by
def assign_risk_level(stations_nearby):
    """Assign risk level based on the analysis"""
    if not stations_nearby:
        return "extremely high risk"
    max_func = max(len(station["functionalities"]) for station in stations_nearby)
    if max_func >= 3:
        return "low risk"
    if max_func == 2:
        return "moderate risk"
    if max_func == 1:
        return "high risk"
    return "undetermined"


def load_station_data(csv_path):
    """Load fire station data from a CSV file."""
    df = pd.read_csv(csv_path)
    stations = []
    for _, row in df.iterrows():
        name = row["Station Name"]
        lat = row["y"]
        lon = row["x"]

        # classify nearest station based on functionality (pumper, ladder, rescue vs headquarter)
        funcs = []
        if "LADDER" in name.upper():
            funcs.append("ladder")
        if "ENGINE" in name.upper():
            funcs.append("pumper")
        if "RESCUE" in name.upper():
            funcs.append("rescue")
        else:
            funcs.append("unknown")

        station = {
            "station_name": name,
            "latitude": lat,
            "longitude": lon,
            "functionalities": funcs,
            "type": "Fire Station"
        }
        stations.append(station)
    return stations


def haversine_distance(user_lat1, user_lon1, station_lat2, station_lon2):
    """Return the distance between two lat/lon points in kilometers."""
    earth_radius_km = 6371.0
    phi1 = math.radians(user_lat1)
    phi2 = math.radians(station_lat2)
    delta_phi = math.radians(station_lat2 - user_lat1)
    delta_lambda = math.radians(station_lon2 - user_lon1)
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earth_radius_km * c


def visualize_stations(
    user_location,
    nearby_stations,
    radius_km=5,
    image_name="map.png",
    output_dir="/app/static",
):
    """Generate and save a map image of the user location and nearby fire stations."""
    _, ax = plt.subplots()
    # Plot user
    ax.scatter(
        user_location["longitude"],
        user_location["latitude"],
        color="red",
        label="User Location",
        zorder=5,
    )
    # Plot nearby fire stations
    for station in nearby_stations:
        ax.scatter(station["longitude"], station["latitude"], color="blue", zorder=3)
        ax.text(
            station["longitude"],
            station["latitude"],
            station["station_name"][:20],
            fontsize=6,
        )
    # Radius circle
    radius_deg = radius_km / 111
    circle = plt.Circle(
        (user_location["longitude"], user_location["latitude"]),
        radius_deg,
        color="gray",
        fill=False,
        linestyle="--",
        label=f"{radius_km}km radius",
    )
    ax.add_patch(circle)
    ax.set_title("User Location and Nearby Fire Stations")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend()
    ax.grid(True)
    plt.axis("equal")
    plt.tight_layout()

    # Create output path
    os.makedirs(output_dir, exist_ok=True)
    image_path = os.path.join(output_dir, image_name)
    plt.savefig(image_path)
    plt.close()
    print(f"Map image saved to {image_path}")
    return image_path

def query_travel_times(user_lat, user_lon, destinations):
    origins = f"{user_lat},{user_lon}"
    destinations = "|".join([f"{lat},{lon}" for lat, lon in destinations])
    
    params = {
        "origins": origins,
        "destinations": destinations,
        "key": GOOGLE_MAPS_API_KEY,
    }
    
    response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json", params=params)
    data = response.json()
    
    clean_data = []
    for i in range(len(data["rows"][0]["elements"])):
        temp_dest = data["rows"][0]["elements"][i]
        if temp_dest["status"] == "OK":
            clean_data.append({
                "destination": data["destination_addresses"][i],
                "distance": temp_dest["distance"]["value"],
                "distance_text": temp_dest["distance"]["text"],
                "duration": temp_dest["duration"]["value"],
                "duration_text": temp_dest["duration"]["text"],
            })
    return clean_data

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    user_location = data.get("user_location")
    if not user_location:
        return jsonify({"error": "Missing user location"}), 400
    result = run_analysis(user_location)
    visualize_stations(
        user_location=user_location,
        nearby_stations=result["nearby_stations"],
        image_name="map.png"
    )
    return jsonify(result)

if __name__ == "__main__":
    # test_tt_user = [40.6947665, -73.9555472]
    # test_tt_dest = [[40.72748565673828, -73.99235534667969], [40.6929079, -73.9485703], [40.693314, -73.9833812]]
    # print(query_travel_times(test_tt_user[0], test_tt_user[1], test_tt_dest))
    app.run(host="0.0.0.0", port=8000)
