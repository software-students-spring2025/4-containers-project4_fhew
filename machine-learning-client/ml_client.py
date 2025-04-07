"""ML client that analyzes data and stores results in MongoDB."""

""" NYC Fire Station Data: https://data.gis.ny.gov/datasets/sharegisny::firestations/about """

""" Other Note: The code must be formatted in accordance with 
[PEP 8](https://www.python.org/dev/peps/pep-0008/) 
using the [black](https://black.readthedocs.io/en/stable/) formatter 
and [pylint](https://pylint.org/) linter to ensure correctness """

from pymongo import MongoClient

# Connect to MongoDB service in Docker
client = MongoClient("mongodb://mongodb:27017")
db = client["sound_data"]
collection = db["analysis"]

# analysis is invoked by the interface of the web app part

def run_analysis():
    # using k-mean algorithm
    sample_data = {
        "audio1": "blue jay",
        "audio2": "owl",
    }
    collection.insert_one(sample_data)
    print("✔️ Data inserted into MongoDB!")

if __name__ == "__main__":
    run_analysis()

# analysis on the nearest fire station

# analysis on nearest station based on functionality (pumper, ladder, rescue vs headquarter)

# assign risk level based on the analysis
    # low risk - surrounded by stations with all functionality
    # moderate risk - surrounded by stations with two functions
    # high risk - surrounded by a single with one function
    # extremly hish risk - no fire station near by

# visualization of the analysis and display to the web app
