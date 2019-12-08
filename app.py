from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

from security import authenticate, identity
from hospital import Hospital, HospitalList

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



api.add_resource(Hospital, '/hospital/<string:name>')
api.add_resource(HospitalList, '/hospitals')

if __name__ == '__main__':
    app.run(debug=True)