from util import db_ex, request
from flask import flash

class User:
    def __init__(self, id):
        table_entry = db_ex(f"SELECT * FROM 'user' WHERE 'user'.id=\"{id}\";").fetchall()
        if len(table_entry) <= 0:
            raise ValueError("You tried to create a user object with an id that is not in the user table")
        else:
            self.id = id
            self.username = table_entry[0][1]
            self.password = table_entry[0][2]
            self.name = table_entry[0][3]
            self.gender = table_entry[0][4]
            self.preference = table_entry[0][5]
            self.dob = table_entry[0][6]
            self.email = table_entry[0][7]
            self.phone_number = table_entry[0][8]
            self.bio = table_entry[0][9]
            self.location = table_entry[0][10]

    def get_starsign(self):
        month = int(self.dob[-5:-3])
        day = int(self.dob[-2:])
        if month == 1:
            if day < 20:
                return "capricorn"
            else:
                return "aquarius"
        elif month == 2:
            if day < 19:
                return "aquarius"
            else:
                return "pisces"
        elif month == 3:
            if day < 21:
                return "aquarius"
            else:
                return "aries"
        elif month == 4:
            if day < 20:
                return "aries"
            else:
                return "taurus"
        elif month == 5:
            if day < 21:
                return "taurus"
            else:
                return "gemini"
        elif month == 6:
            if day < 21:
                return "gemini"
            else:
                return "cancer"
        elif month == 7:
            if day < 23:
                return "cancer"
            else:
                return "leo"
        elif month == 8:
            if day < 23:
                return "leo"
            else:
                return "virgo"
        elif month == 9:
            if day < 23:
                return "virgo"
            else:
                return "libra"
        elif month == 10:
            if day < 23:
                return "libra"
            else:
                return "scorpio"
        elif month == 11:
            if day < 22:
                return "scorpio"
            else:
                return "sagittarius"
        else:
            if day < 22:
                return "sagittarius"
            else:
                return "capricorn"

    # returns a list of user ids of users whom to no request has been sent by the user
    # and whom have not sent a request to the user
    def unmatched(self):
        query = db_ex(f"""SELECT id
        FROM 'user' WHERE NOT 'user'.id = {self.id} EXCEPT SELECT * FROM
        (SELECT sender_id FROM 'request' WHERE 'request'.reciever_id = {self.id}
        UNION SELECT reciever_id FROM 'request' WHERE 'request'.sender_id = {self.id});""").fetchall()
        ret = []
        for response in query:
            ret.append(response[0])
        return ret

    #returns request ids of pending requests sent by user
    def sent_pending(self):
        query = db_ex(f"SELECT request_id FROM 'request' WHERE 'request'.sender_id=\"{self.id}\" AND 'request'.status=\"pending\";").fetchall()
        ret = []
        for response in query:
            ret.append(response[0])
        return ret

    #returns request ids of pending requests recieved by user
    def recieved_pending(self):
        query = db_ex(f"SELECT request_id FROM 'request' WHERE 'request'.reciever_id=\"{self.id}\" AND 'request'.status=\"pending\";").fetchall()
        ret = []
        for response in query:
            ret.append(response[0])
        return ret

    #returns request ids of accepted requests sent or recieved by user that have been accepted
    def accepted(self):
        query = db_ex(f"SELECT request_id FROM 'request' WHERE 'request'.reciever_id=\"{self.id}\" AND 'request'.status=\"accepted\";").fetchall()
        ret = []
        for response in query:
            ret.append(response[0])
        query = db_ex(f"SELECT request_id FROM 'request' WHERE 'request'.sender_id=\"{self.id}\" AND 'request'.status=\"accepted\";").fetchall()
        for response in query:
            ret.append(response[0])
        return ret

    @staticmethod
    def new_user(username, password, name, gender, preference, dob, email, phone_number, bio, location):
        if len(db_ex(f"SELECT * FROM 'user' WHERE 'user'.username=\"{username}\";").fetchall()) > 0:
            flash("username has been taken")
            return False
        else:
            db_ex(f"""INSERT INTO 'user' (username, password, name, gender, preference, dob, email, phone_number, bio, location)
                  VALUES (\"{username}\", \"{password}\", \"{name}\", \"{gender}\", \"{preference}\",
                   \"{dob}\", \"{email}\", \"{phone_number}\", \"{bio}\", \"{location}\");""")
            return True

    @staticmethod
    def get_by_username(username):
        fetch = db_ex(f"SELECT id FROM 'user' WHERE 'user'.username=\"{username}\";").fetchall()
        if len(fetch) == 0:
            raise ValueError("user with that username has not been found")
        else:
            return fetch[0][0]

    @staticmethod
    def query_by_id(userID, query):
        fetch = db_ex(f"SELECT {query} FROM 'user' WHERE 'user'.id = {userID};").fetchall()
        if(len(fetch) == 0):
            flash("Username not found, or error with query")
        return fetch[0][0]

    @staticmethod
    def authenticate_user(username, password):
        fetch = db_ex(f"SELECT password FROM 'user' WHERE 'user'.username=\"{username}\";").fetchall()
        if len(fetch) == 0:
            flash("Username not found")
            return False #user with that username does not exist
        if fetch[0][0] != password:
            flash("Incorrect password")
            return False
        else:
            print(fetch)
            return True
