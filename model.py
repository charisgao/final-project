import random

def random_num(data):
    return random.randint(0, len(data)-1)

def name(data, num):
    return data[num]["name"]

def picture(data, num):
    return data[num][""]

def coordinates(data, num):
    return data[num]["coordinates"] #latitude, longitude