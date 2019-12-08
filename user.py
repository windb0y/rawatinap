#import MySQLdb
import mysql.connector

#SQL connection data to connect and save the data in
HOST = "localhost"
USERNAME = "root"
PASSWORD = ""
DATABASE = "scraping_sample"

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = mysql.connector.connect(host=HOST, database=DATABASE, user=USERNAME, passwd=PASSWORD)
        cursor = connection.cursor()

        query = "SELECT * FROM user WHERE username=%s"
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
        connection = mysql.connector.connect(host=HOST, database=DATABASE, user=USERNAME, passwd=PASSWORD)
        cursor = connection.cursor()

        query = "SELECT * FROM user WHERE id=%s"
        result = cursor.execute(query, (_id,))
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user