import urllib3
import json
from skyfield.api import load

http = urllib3.PoolManager()
planets = load("de421.bsp")
time = load.timescale()

def mercury(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["mercury barycenter"]).position.au

def venus(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["venus barycenter"]).position.au

def mars(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["mars barycenter"]).position.au

def jupiter(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["jupiter barycenter"]).position.au

def saturn(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["saturn barycenter"]).position.au

def uranus(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["uranus barycenter"]).position.au

def neptune(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["neptune barycenter"]).position.au

def pluto(year, month, day):
    t = time.utc(int(year), int(month), int(day))
    return planets["sun"].at(t).observe(planets["pluto barycenter"]).position.au

def ohmanda(sunsign):
    request = http.request("GET", f"http://ohmanda.com/api/horoscope/{sunsign}")
    return request.data.decode('utf-8')

def json2dict(json):
    return json.loads(json)

def dict2json(dict):
    return json.dump(dict)
