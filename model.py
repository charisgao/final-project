import random

def random_num(data, days):
    return random.sample(range(0, len(data) - 1), days)

def name(data, num):
    return data[num]["name"]

def picture(data, num):
    return data[num]["image_url"]

def coordinates(data, num):
    return data[num]["coordinates"] #latitude, longitude