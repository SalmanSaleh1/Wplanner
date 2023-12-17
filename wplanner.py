from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import openmeteo_requests
import requests_cache
from retry_requests import retry
import numpy as np

app = Flask(__name__)

# MongoDB configurations
HOSTNAME = "wplanner_mongodb"
DATABASE_NAME = "wplanner_db"
COLLECTION_NAME = "wplanner_collection"

client = MongoClient(host=HOSTNAME, port=27017)
db = client[DATABASE_NAME][COLLECTION_NAME]

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(backend='memory', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


@app.route('/wplanner', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def wplanner():
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        place = request.form['place']

        # Fetch weather information using Open-Meteo API
        latitude, longitude = get_coordinates_for_place(place)
        weather_info = get_weather_info(latitude, longitude)

        # Store the plan in MongoDB
        store_plan(date, description, place, weather_info)

    plans = get_plans_from_db()
    return render_template('wplanner.html', plans=plans)


# About route
@app.route('/about')
def about():
    return render_template('about.html')


# Define the /get_weather_info route
@app.route('/get_weather_info', methods=['GET'])
def get_weather_info_for_submission():
    if request.method == 'GET':
        # Extract latitude and longitude from the request.args
        place = request.args.get('place')
        latitude, longitude = get_coordinates_for_place(place)

        # Fetch weather information using Open-Meteo API
        weather_info = get_weather_info(latitude, longitude)

        # Return the weather information as JSON
        return jsonify({'status': 'success', 'weather_info': weather_info})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request method'})


def get_coordinates_for_place(place):
    # Coordinates for locations in Saudi Arabia
    saudi_arabia_coordinates = {
        "Riyadh": (24.68773, 46.72185),
        "Jeddah": (21.49012, 39.18624),
        "Mecca": (21.42664, 39.82563),
        "Medina": (24.46861, 39.61417),
        "Dammam": (26.43442, 50.10326),
        "Sulţānah": (24.49258, 39.58572),
        "Tabuk": (28.3998, 36.57151),
        "Buraydah": (26.32599, 43.97497),
        "Al Mubarraz": (25.40768, 49.59028),
        "Ta’if": (21.27028, 40.41583),
        "Najran": (17.49326, 44.12766),
        "Al Kharj": (24.15541, 47.33457),
        "Abha": (18.21639, 42.50528),
        "Yanbu": (24.08954, 38.0618),
        "Khamis Mushait": (18.3, 42.73333),
        "Al Hufūf": (25.36467, 49.58764),
        "Hafar Al-Batin": (28.43279, 45.97077),
        "Ha'il": (27.52188, 41.69073),
        "Ar Rass": (25.86944, 43.4973),
        "Al Jubayl": (27.0174, 49.62251),
    }

    return saudi_arabia_coordinates.get(place, (0, 0))  # Default to (0, 0) if place not found


def get_weather_info(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,wind_speed_10m,cloud_cover"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process all responses (assuming there might be multiple locations)
    all_hourly_temperature_2m = []
    all_hourly_wind_speed = []
    all_hourly_cloud_cover = []

    for response in responses:
        hourly_temperature_2m = response.Hourly().Variables(0).ValuesAsNumpy()
        hourly_wind_speed = response.Hourly().Variables(1).ValuesAsNumpy()
        hourly_cloud_cover = response.Hourly().Variables(2).ValuesAsNumpy()

        all_hourly_temperature_2m.append(hourly_temperature_2m)
        all_hourly_wind_speed.append(hourly_wind_speed)
        all_hourly_cloud_cover.append(hourly_cloud_cover)

    # Calculate daily averages
    daily_average = {
        "temperature_2m": float(np.concatenate(all_hourly_temperature_2m).mean()),
        "wind_speed_10m": float(np.concatenate(all_hourly_wind_speed).mean()),
        "cloud_cover": float(np.concatenate(all_hourly_cloud_cover).mean())
    }

    return daily_average


def store_plan(date, description, place, weather_info):
    plan = {
        "date": date,
        "description": description,
        "place": place,
        "weather_info": weather_info
    }
    db.plans.insert_one(plan)


def get_plans_from_db():
    # Use aggregation to group plans by date and select the most recent one for each date
    pipeline = [
        {"$sort": {"date": -1}},  # Sort by date in descending order
        {"$group": {"_id": "$date", "plans": {"$push": "$$ROOT"}}},
        {"$replaceRoot": {"newRoot": {"$arrayElemAt": ["$plans", -1]}}}
    ]

    plans_cursor = db.plans.aggregate(pipeline)
    plans = list(plans_cursor)

    # Sort the plans by date in ascending order
    plans.sort(key=lambda x: x['date'])

    return plans


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)