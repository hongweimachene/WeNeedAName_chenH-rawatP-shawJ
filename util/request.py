from util import db_ex
from flask import flash

class Request:
    def __init__(self, id):
        table_entry = db_ex(f"SELECT * FROM 'request' WHERE 'request'.request_id=\"{id}\";").fetchall()
        if len(table_entry) <= 0:
            raise ValueError("You tried to create a request object with an id that is not in the request table")
        else:
            self.request_id = id
            self.sender_id = table_entry[0][1]
            self.reciever_id = table_entry[0][2]
            self.status = table_entry[0][3]
            self.message = table_entry[0][4]


    @staticmethod
    def new_request(sender_id, reciever_id, status, message):
        if len(db_ex(f"SELECT * FROM 'request' WHERE 'request'.sender_id=\"{sender_id}\" AND 'request'.reciever_id=\"{reciever_id}\";").fetchall()) > 0:
            flash("a request has already been sent to this person")
            return False
        else:
            db_ex(f"""INSERT INTO 'request' (sender_id, reciever_id, status, message)
                  VALUES ({sender_id}, {reciever_id}, {status}, \"{message}\");""")
            return True

    @staticmethod
    def get_by_sender(sender_id):
        fetch = db_ex(f"SELECT request_id FROM 'request' WHERE 'request'.sender_id=\"{sender_id}\";").fetchall()
        return fetch[0]

    @staticmethod
    def get_by_reciever(reciever_id):
        fetch = db_ex(f"SELECT reciever_id FROM 'request' WHERE 'request'.reciever_id=\"{reciever_id}\";").fetchall()
        return fetch[0]
