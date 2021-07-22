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

    days = request.form["days"]

    # RESTAURANT
    PARAMETERS = {"term": "restaurants", "limit" : 50, "location": request.form["location"]}
    # Make a request to the Yelp API
    restaurant_response = requests.get(url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
    # Convert a JSON string to a dictionary
    restaurant_data = restaurant_response.json()

    restaurants = restaurant_data["businesses"]

    restaurant_nums = []
    for day in range(int(days)):
        for num in range(3):
            restaurant_nums.append(model.random_num(restaurants))

    restaurant_list = []
    for number in range(3 * int(days)):
            restaurant_list.append(
                {
                    "name": model.name(restaurants, restaurant_nums[number]),
                    "picture": model.picture(restaurants, restaurant_nums[number]),
                    "coordinates": model.coordinates(restaurants, restaurant_nums[number])
                }
            )

    # HOTEL
    PARAMETERS = {"term": "hotels", "limit" : 50, "location": request.form["location"]}
    hotel_response = requests.get(url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
    hotel_data = hotel_response.json()

    hotels = hotel_data["businesses"]

    hotel_nums = []
    for day in range(int(days)):
        hotel_nums.append(model.random_num(hotels))
    
    hotel_list = []
    for number in range(int(days)):
            hotel_list.append(
                {
                    "name": model.name(hotels, hotel_nums[number]),
                    "picture": model.picture(hotels, hotel_nums[number]),
                    "coordinates": model.coordinates(hotels, hotel_nums[number])
                }
            )

    # THINGS TO DO
    PARAMETERS = {"term": "things to do", "limit" : 50, "location": request.form["location"]}
    thingstodo_response = requests.get(url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
    thingstodo_data = thingstodo_response.json()

    thingstodo = thingstodo_data["businesses"]

    thingstodo_nums = []
    for day in range(int(days)):
        for num in range(2):
            thingstodo_nums.append(model.random_num(thingstodo))
    
    thingstodo_list = []
    for number in range(int(days)):
            thingstodo_list.append(
                {
                    "name": model.name(thingstodo, thingstodo_nums[number]),
                    "picture": model.picture(thingstodo, thingstodo_nums[number]),
                    "coordinates": model.coordinates(thingstodo, thingstodo_nums[number])
                }
            )

    return render_template("results.html", days=days, restaurants=restaurant_list, hotels=hotel_list, thingstodo=thingstodo_list, google_key=GOOGLE_API)
