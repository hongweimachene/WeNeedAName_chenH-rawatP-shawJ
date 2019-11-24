import sqlite3

file = "horoscope_dating.db"

def db_ex(cmd):
    db = sqlite3.connect(file) #open if file exists, otherwise create
    c = db.cursor()
    out = c.execute(cmd)
    db.commit()
    return out

def db_setup():
    # db_ex("DROP TABLE IF EXISTS \"user\"")
    # db_ex("DROP TABLE IF EXISTS \"request\"")
    db_ex("""CREATE TABLE IF NOT EXISTS 'user'
             (id INTEGER PRIMARY KEY NOT NULL,
             username VARCHAR,
             password VARCHAR,
             name VARCHAR,
             gender VARCHAR,
             preference VARCHAR,
             dob TIMESTAMP,
             email VARCHAR,
             phone_number VARCHAR,
             bio VARCHAR,
             horoscope_info VARCHAR);""")
    db_ex("""CREATE TABLE IF NOT EXISTS 'request'
             (request_id INTEGER PRIMARY KEY NOT NULL,
             sender_id INTEGER,
             reciever_id INTEGER,
             status VARCHAR,
             message VARCHAR);""")
