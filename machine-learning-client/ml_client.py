"""ML client that analyzes data and stores results in MongoDB."""

from pymongo import MongoClient

# Connect to MongoDB service in Docker
client = MongoClient("mongodb://mongodb:27017")
db = client["sound_data"]
collection = db["analysis"]

def run_analysis():
    sample_data = {
        "audio1": "blue jay",
        "audio2": "owl",
    }
    collection.insert_one(sample_data)
    print("✔️ Data inserted into MongoDB!")

if __name__ == "__main__":
    run_analysis()