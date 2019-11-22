import urllib3
import json

http = urllib3.PoolManager()

# def ephemermis(yearOfBirth, monthOfBirth, dayOfBirth):
#     request = http.request("GET", """https://private-anon-9e3b1e376f-astrologyapi.apiary-mock.com/planets&data={
#     "event": "{}{}{}0000000",
#     "planets": ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Chiron", "Lilith", "NNode"],
#     "topo": [ longitude, latitude, geoalt],"zodiac": "sidereal mode name"
#     }&headers={'Content-Type': 'application/json','Accept': 'application/json'}""".format(yearOfBirth, monthOfBirth, dayOfBirth))
#     return request.data

def ephemermis(yearOfBirth, monthOfBirth, dayOfBirth):
    request = http.request("GET", """https://json.astrologyapi.com/v1/planets""".format(yearOfBirth, monthOfBirth, dayOfBirth))
    return request.data

def ohmanda(sunsign):
    request = http.request("GET", "http://ohmanda.com/api/horoscope/".format(sunsign))
    return request.data

def json2dict(json):
    return json.loads(json)

def dict2json(dict):
    return json.dump(dict)
