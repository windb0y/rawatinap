from flask import Flask, jsonify
from flask_restful import Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
import mysql.connector
import psycopg2
from security import authenticate, identity
from hospital import Hospital, HospitalList, BedList


#SQL connection data to connect and save the data in
HOST = "ec2-174-129-255-72.compute-1.amazonaws.com"
USERNAME = "mhlrnhivjvoetu"
PASSWORD = "ebdd3e33788bc7bce152f1aac9e207c41f418afb9e02e5638911d2799790adae"
DATABASE = "d4h05h6uurju86"
'''
hospitals = [
    {
        'code': '3489076',
        'name': 'RS Harapan Bunda',
        'type': 'RS Vertikal',
        'province': 'DKI Jakarta',
        'total_bed': 200,
        'used_bed': 150,
        'empty_bed': 50
    }
]
'''
app = Flask(__name__)
app.secret_key = 'hospital'
api = Api(app)

jwt = JWT(app, authenticate, identity)

@app.route('/') #https://windboyshare.com/rawatinap
def home():
    return """
    <h1>API Ketersediaan tempat tidur di rumah sakit </h1>
    <h3>untuk memberikan informasi publik tentang ketersedian tempat tidur di berbagai rumah sakit</h3>
    <h3>API's base URL</h3>
    <h4>Authentifikasi</h4>
    <code>/auth</code>
    """
# GET /hospital
@app.route('/hospital')
def get_hospitals():
    connection = psycopg2.connect(host=HOST, user=USERNAME, password=PASSWORD, dbname=DATABASE)
    cursor = connection.cursor()

    query = "SELECT * FROM rumah_sakit"
    cursor.execute(query)
    data = cursor.fetchall()
    hospital = []

    for row in data:
        hospital.append({'code': row[1], 'name': row[2], 'type': row[4], 'province': row[3], 'total_bed': row[5], 'used_bed': row[6], 'empty_bed': row[7], 'timestamp': row[8].strftime("%m/%d/%Y, %H:%M:%S")})

    connection.close

    return jsonify({'hospital': hospital}) 


api.add_resource(HospitalList, '/hospitals')

api.add_resource(Hospital, '/hospital/<string:name>')

api.add_resource(BedList, '/hospitals/bed')

if __name__ == '__main__':
    app.run(debug=True)