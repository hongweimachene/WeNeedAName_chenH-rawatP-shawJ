from util import db_ex

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
            self.dob = table_entry[0][4]
            self.email = table_entry[0][5]
            self.phone_number = table_entry[0][6]
            self.bio = table_entry[0][7]
            self.horoscope_info = table_entry[0][8]

    @staticmethod
    def new_user(username, password, name, dob, email, phone_number, bio, horoscope_info):
        if db_ex(f"SELECT id FROM 'user' WHERE 'user'.username=\"{username}\";").fetchall() > 0:
            raise ValueError("username has been taken")
        else:
            db_ex(f"""INSERT INTO 'user' (username, password, name, dob, email, phone_number, bio, horoscope_info)
                  VALUES (\"{username}\", \"{password}\", \"{name}\", \"{dob}\", \"{email}\",
                  \"{phone_number}\", \"{bio}\", \"{horoscope_info}\");""")

    @staticmethod
    def get_by_username(username):
        fetch = db_ex(f"SELECT id FROM 'user' WHERE 'user'.username=\"{username}\";").fetchall()
        if len(fetch) == 0:
            raise ValueError("user with that username has not been found")
        else:
            return fetch[0][0]

    @staticmethod
    def authenticate_user(username, password):
        fetch = db_ex(f"SELECT password FROM 'user' WHERE 'user'.username=\"{username}\";").fetchall()
        if len(fetch) == 0:
            return -1 #user with that username does not exist
        if lenfetch[0][0] != password:
            return 0 #password is incorrect
        else:
            return 1 #user authenticated
