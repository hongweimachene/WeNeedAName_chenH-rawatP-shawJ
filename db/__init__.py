import sqlite3

file = "horoscope_dating.db"

def db_ex(cmd):
    db = sqlite3.connect(file) #open if file exists, otherwise create
    c = db.cursor()
    c.execute(cmd)
    db.commit()

def db_setup():
    db_ex("DROP TABLE IF EXISTS \"user\"")
    db_ex("DROP TABLE IF EXISTS \"request\"")
    db_ex("""CREATE TABLE IF NOT EXISTS 'user'
             (id INT PRIMARY KEY,
             username VARCHAR,
             password VARCHAR,
             name VARCHAR,
             dob TIMESTAMP,
             email VARCHAR,
             phone_number VARCHAR,
             bio VARCHAR,
             horoscope_info VARCHAR);""")
    db_ex("""CREATE TABLE IF NOT EXISTS 'request'
             (request_id INT PRIMARY KEY,
             sender_id INT,
             reciever_id INT,
             status VARCHAR,
             message VARCHAR);""")
