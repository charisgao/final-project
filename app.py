# Imports
from flask import Flask, render_template, request
from datetime import datetime
import model
import os   # allows us to access environmental variables that we want to keep hidden
import requests

# Initialization
app = Flask(__name__)

# Define the endpoint and headers for yelp API key
app.config["YELP_KEY"] = os.getenv("YELP_KEY")
YELP_API = app.config["YELP_KEY"]
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % YELP_API}

# Google API key
app.config["GOOGLE_KEY"] = os.getenv("GOOGLE_KEY")
GOOGLE_API = app.config["GOOGLE_KEY"]

# Routes


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", time=datetime.now())


@app.route('/results', methods=["GET", "POST"])
def results():
    # RESTAURANT
    PARAMETERS = {"term": "restaurants", "location": request.form["location"]}
    # Make a request to the Yelp API
    restaurant_response = requests.get(
        url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
    # Convert a JSON string to a dictionary
    restaurant_data = restaurant_response.json()

    restaurants = restaurant_data["businesses"]

    restaurant_nums = []
    days = request.form["days"]
    for day in days:
        for num in range(3):
            restaurant_nums.append(model.random_num(restaurants))

    restaurant_list = []
    for number in 3 * days:
            restaurant_list.append(
                {
                    "name": model.name(restaurants, restaurant_nums[num]),
                    "picture": model.picture(restaurants, restaurant_nums[num]),
                    "coordinates": model.coordinates(restaurants, restaurant_nums[num])
                }
            )

    # HOTEL
    PARAMETERS = {"term": "hotels", "location": request.form["location"]}
    hotel_response = requests.get(
        url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
    hotel_data = hotel_response.json()

    hotels = hotel_data["businesses"]

    hotel_nums = []
    for day in days:
        hotel_nums.append(model.random_num(hotels))

    # THINGS TO DO
    PARAMETERS = {"term": "things to do", "location": request.form["location"]}
    thingstodo_response = requests.get(
        url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
    thingstodo_data = thingstodo_response.json()

    return render_template("results.html", data=restaurants, restaurants=restaurant_list, google_key=GOOGLE_API)
