import mysql.connector
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

#SQL connection data to connect and save the data in
HOST = "localhost"
USERNAME = "root"
PASSWORD = ""
DATABASE = "scraping_sample"

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

class Hospital(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('total_bed',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        connection = mysql.connector.connect(host=HOST, database=DATABASE, user=USERNAME, passwd=PASSWORD)
        cursor = connection.cursor()

        query = "SELECT * FROM rumah_sakit WHERE nama_rs=%s"
        cursor.execute(query, (name,))
        row = cursor.fetchone()
        connection.close

        if row:
            return {'hospital': {'code': row[1], 'name': row[2], 'type': row[4], 'province': row[3], 'total_bed': row[5], 'used_bed': row[6], 'empty_bed': row[7], 'timestamp': row[8].strftime("%m/%d/%Y, %H:%M:%S")}}
        return {'message': 'hospital not found'}
        
    @jwt_required()
    def post(self, name):
        #if next(filter(lambda x: x['name'] == name, hospitals), None) is not None:
        #    return {'message': "A hospital with name '{}' already exists.".format(name)}

        data = Hospital.parser.parse_args()

        hospital = {'name': name, 'total_bed': data['total_bed']}
        
        connection = mysql.connector.connect(host=HOST, database=DATABASE, user=USERNAME, passwd=PASSWORD)
        cursor = connection.cursor()

        query = "INSERT INTO rumah_sakit (nama_rs, tempat_tidur_total) VALUES (%s, %s)"
        cursor.execute(query, (hospital['name'], hospital['total_bed']))

        connection.commit()
        connection.close()

        return hospital, 201
    '''
    @jwt_required()
    def delete(self, name):
        global hospitals
        hospitals = list(filter(lambda x: x['name'] != name, hospitals))
        return {'message': 'hospital deleted'}

    @jwt_required()
    def put(self, name):
        data = Hospital.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        hospital = next(filter(lambda x: x['name'] == name, hospitals), None)
        if hospital is None:
            hospital = {'name': name, 'price': data['price']}
            hospitals.append(hospital)
        else:
            hospital.update(data)
        return hospital
    '''

class HospitalList(Resource):
    def get(self):
        connection = mysql.connector.connect(host=HOST, database=DATABASE, user=USERNAME, passwd=PASSWORD)
        cursor = connection.cursor()

        query = "SELECT * FROM rumah_sakit"
        cursor.execute(query)
        data = cursor.fetchall()
        hospital = []

        for row in data:
            hospital.append({'code': row[1], 'name': row[2], 'type': row[4], 'province': row[3], 'total_bed': row[5], 'used_bed': row[6], 'empty_bed': row[7], 'timestamp': row[8].strftime("%m/%d/%Y, %H:%M:%S")})

        connection.close

        return {'hospital': hospital}

class BedList(Resource):
    def get(self):
        connection = mysql.connector.connect(host=HOST, database=DATABASE, user=USERNAME, passwd=PASSWORD)
        cursor = connection.cursor()

        query = "SELECT * FROM rumah_sakit WHERE tempat_tidur_total > tempat_tidur_isi"
        cursor.execute(query)
        data = cursor.fetchall()
        hospital = []

        for row in data:
            hospital.append({'code': row[1], 'name': row[2], 'type': row[4], 'province': row[3], 'total_bed': row[5], 'used_bed': row[6], 'empty_bed': row[7], 'timestamp': row[8].strftime("%m/%d/%Y, %H:%M:%S")})

        connection.close

        return {'hospital': hospital}

