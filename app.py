from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

from security import authenticate, identity
from hospital import Hospital, HospitalList, BedList

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

api.add_resource(Hospital, '/hospital/<string:name>')
api.add_resource(HospitalList, '/hospitals')
api.add_resource(BedList, '/hospitals/bed')

if __name__ == '__main__':
    app.run(debug=True)