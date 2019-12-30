#import MySQLdb
import mysql.connector
import psycopg2

#SQL connection data to connect and save the data in
#HOST = "localhost"
#USERNAME = "postgres"
#PASSWORD = "root"
#DATABASE = "rawatinap"

HOST = "ec2-174-129-255-72.compute-1.amazonaws.com"
USERNAME = "mhlrnhivjvoetu"
PASSWORD = "ebdd3e33788bc7bce152f1aac9e207c41f418afb9e02e5638911d2799790adae"
DATABASE = "d4h05h6uurju86"

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = psycopg2.connect(host=HOST, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=%s"
        result = cursor.execute(query, (username,))
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()  
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = psycopg2.connect(host=HOST, user=USERNAME, password=PASSWORD, dbname=DATABASE)
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=%s"
        result = cursor.execute(query, (_id,))
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user