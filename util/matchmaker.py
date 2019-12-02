import util.api_request
from random import random

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

def personalityCompatibility(person1, person2):
    try:
        p1Pos = util.api_request.mercury(person1.yearOfBirth, person1.monthOfBirth, person1.dayOfBirth)
        p2Pos = util.api_request.mercury(person2.yearOfBirth, person2.monthOfBirth, person2.dayOfBirth)
        return p1Pos[0] + p1Pos[1] + p1Pos[2] / p2Pos[0] + p2Pos[1] + p2Pos[2]
    except:
        return random()

def sexualCompatibility(person1, person2):
    try:
        p1Pos = util.api_request.mars(person1.yearOfBirth, person1.monthOfBirth, person1.dayOfBirth)
        p2Pos = util.api_request.mars(person2.yearOfBirth, person2.monthOfBirth, person2.dayOfBirth)
        return p1Pos[0] + p1Pos[1] + p1Pos[2] / p2Pos[0] + p2Pos[1] + p2Pos[2]
    except:
        return random()

def inLawsCompatibility(person1, person2):
    try:
        p1Pos = util.api_request.jupiter(person1.yearOfBirth, person1.monthOfBirth, person1.dayOfBirth)
        p2Pos = util.api_request.jupiter(person2.yearOfBirth, person2.monthOfBirth, person2.dayOfBirth)
        return p1Pos[0] + p1Pos[1] + p1Pos[2] / p2Pos[0] + p2Pos[1] + p2Pos[2]
    except:
        return random()

def futureSuccess(person1, person2):
    try:
        p1Pos = util.api_request.saturn(person1.yearOfBirth, person1.monthOfBirth, person1.dayOfBirth)
        p2Pos = util.api_request.saturn(person2.yearOfBirth, person2.monthOfBirth, person2.dayOfBirth)
        return p1Pos[0] + p1Pos[1] + p1Pos[2] / p2Pos[0] + p2Pos[1] + p2Pos[2]
    except:
        return random()

class Person(object):

    yearOfBirth = 0
    monthOfBirth = 0
    dayOfBirth = 0

    def __init__(self, yearOfBirth, monthOfBirth, dayOfBirth):
        super(Person, self).__init__()
        self.yearOfBirth = yearOfBirth
        self.monthOfBirth = monthOfBirth
        self.dayOfBirth = dayOfBirth
