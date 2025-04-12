![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![Web App CI](https://github.com/software-students-spring2025/4-containers-project4_fhew/actions/workflows/web-app.yml/badge.svg?branch=)
![ML Client CI](https://github.com/software-students-spring2025/4-containers-project4_fhew/actions/workflows/ml-client.yml/badge.svg?branch=)

# Fire Station Locator 

A web application designed for homebuyers, renters, and visitors of New York City to assess their proximity to emergency fire services. Our app helps users make informed decisions about where to live or stay by letting them know if they're within a reasonable distance of a fire station. 


## Team Members
- [Forrest Williams](https://github.com/Zeklin)
- [Wyatt Destabelle](https://github.com/Wyatt-Destabelle)
- [Helen Ho](https://github.com/hhelenho)
- [Emily Ney](https://github.com/EmilyNey)


## Features
- Collects user location through the browser.
- Identifies the five closest NYC fire stations.
- Displays nearby fire stations with estimated travel time and distance.
- Visualizes locations on an interactive map.
- Machine learning client processes proximity and analyzes risk.
- Data from [NYC Open Data](https://data.gis.ny.gov/datasets/sharegisny::firestations/about).


## How to Run This Project


### Setup
1. **Clone the repository**
```bash
git clone https://github.com/software-students-spring2025/4-containers-project4_fhew.git
cd 4-containers-project4_fhew
```

2. **Environment Setup** 
Create a `.env` filie in the `machine-learning-client/` directory following this example: 
```
GOOGLE_MAPS_API_KEY=your_google_api_key
```

This is used by `config.py` to enable travel time functionality through Google Maps. 

3. **Build and Start the App**
```bash
docker compose up --build
```
This command builds both the *web-app* and *machine-learning-client* services and installs the required packages using the `Pipfile` and `requirements.txt`

The web application will be available at `http://localhost:5002`

The machine learning service runs on `http://localhost:8000`


## Data Source
`firestations_info.csv` - downloadable location data sourced from [NYC GIS Open Data](https://data.gis.ny.gov/datasets/sharegisny::firestations/about)


## Note to Developers
To run tests:
```
cd web-app && pytest
cd machine-learning-client && pytest
```