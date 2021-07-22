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
HEADERS = {'Authorization' : 'bearer %s' % YELP_API}

# Google API key
app.config["GOOGLE_KEY"] = os.getenv("GOOGLE_KEY")
GOOGLE_API = app.config["GOOGLE_KEY"]

# Routes
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", time = datetime.now())

@app.route('/results', methods=["GET", "POST"])
def results():
    # Define the parameters
    PARAMETERS = {"term" : "restaurants", "location" : request.form["location"]}
    # Make a request to the Yelp API
    response = requests.get(url = ENDPOINT, params = PARAMETERS, headers = HEADERS)
    # Convert a JSON string to a dictionary
    business_data = response.json()

    data = business_data["businesses"]
    coordinates = model.coordinates(data)

    return render_template("results.html", data = data, coordinates = coordinates, google_key = GOOGLE_API)