import urllib3
import json
from skyfield.api import load

http = urllib3.PoolManager()
planets = load("de421.bsp")
time = load.timescale()

def mercury(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["mercury"]).position.au

def venus(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["venus"]).position.au

def mars(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["mars"]).position.au

def jupiter(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["jupiter"]).position.au

def saturn(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["saturn"]).position.au

def uranus(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["uranus"]).position.au

def neptune(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["neptune"]).position.au

def pluto(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["pluto"]).position.au

# def ephemermis(yearOfBirth, monthOfBirth, dayOfBirth):
#     request = http.request("GET", """https://private-anon-9e3b1e376f-astrologyapi.apiary-mock.com/planets&data={
#     "event": "{}{}{}0000000",
#     "planets": ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron", "Lilith", "NNode"],
#     "topo": [ longitude, latitude, geoalt],"zodiac": "sidereal mode name"
#     }&headers={'Content-Type': 'application/json','Accept': 'application/json'}""".format(yearOfBirth, monthOfBirth, dayOfBirth))
#     return request.data

def astrology(yearOfBirth, monthOfBirth, dayOfBirth):
    request = http.request("GET", """https://json.astrologyapi.com/v1/planets""".format(yearOfBirth, monthOfBirth, dayOfBirth))
    return request.data

def ohmanda(sunsign):
    request = http.request("GET", "http://ohmanda.com/api/horoscope/".format(sunsign))
    return request.data

def json2dict(json):
    return json.loads(json)

def dict2json(dict):
    return json.dump(dict)
