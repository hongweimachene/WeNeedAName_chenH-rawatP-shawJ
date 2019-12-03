import util.api_request
from random import random, seed

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

def personalityCompatibility(person1, person2):
    '''Using position of mercury based on user date of birth, we are determining the compatability of the personalities of the users'''
    try:
        p1Pos = util.api_request.mercury(person1.yearOfBirth, person1.monthOfBirth, person1.dayOfBirth)
        p2Pos = util.api_request.mercury(person2.yearOfBirth, person2.monthOfBirth, person2.dayOfBirth)
        random.seed(p1Pos[0] + p1Pos[1] + p1Pos[2] + p2Pos[0] + p2Pos[1] + p2Pos[2])
        return random()
    except:
        return random()

def sexualCompatibility(person1, person2):
    '''Using position of mars based on user date of birth, we are determing the sexual compatability of the users'''
    try:
        p1Pos = util.api_request.mars(person1.yearOfBirth, person1.monthOfBirth, person1.dayOfBirth)
        p2Pos = util.api_request.mars(person2.yearOfBirth, person2.monthOfBirth, person2.dayOfBirth)
        random.seed(p1Pos[0] + p1Pos[1] + p1Pos[2] + p2Pos[0] + p2Pos[1] + p2Pos[2])
        return random()
    except:
        return random()

def inLawsCompatibility(person1, person2):
    '''Using position of jupiter based on user date of birth, we are determing the in laws compabilitiy of the users'''
    try:
        p1Pos = util.api_request.jupiter(person1.yearOfBirth, person1.monthOfBirth, person1.dayOfBirth)
        p2Pos = util.api_request.jupiter(person2.yearOfBirth, person2.monthOfBirth, person2.dayOfBirth)
        random.seed(p1Pos[0] + p1Pos[1] + p1Pos[2] + p2Pos[0] + p2Pos[1] + p2Pos[2])
        return random()
    except:
        return random()

def futureSuccess(person1, person2):
    '''Calculates future success of users using position of saturn based on user date of birth'''
    try:
        p1Pos = util.api_request.saturn(person1.yearOfBirth, person1.monthOfBirth, person1.dayOfBirth)
        p2Pos = util.api_request.saturn(person2.yearOfBirth, person2.monthOfBirth, person2.dayOfBirth)
        random.seed(p1Pos[0] + p1Pos[1] + p1Pos[2] + p2Pos[0] + p2Pos[1] + p2Pos[2])
        return random()
    except:
        return random()

'''Class to store a user's d.o.b. info''' 
class Person(object):

    yearOfBirth = 0
    monthOfBirth = 0
    dayOfBirth = 0

    def __init__(self, yearOfBirth, monthOfBirth, dayOfBirth):
        super(Person, self).__init__()
        self.yearOfBirth = yearOfBirth
        self.monthOfBirth = monthOfBirth
        self.dayOfBirth = dayOfBirth
