"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200


@app.route('/people', methods=['POST', 'GET'])
def manage_people():
    data = {}
    if request.method == 'POST':
        data = {"status" : "The user was created"}
        data = request.get_json()
        
        user1 = Person(username=data['username'], email=data['email'])
        db.session.add(user1)
        db.session.commit()

    if request.method == 'GET':
        people_query = Person.query.all()
        data = list(map(lambda x: x.serialize(), people_query))

    return jsonify(data), 200

@app.route('/people/<int:person_id>', methods=['PUT', 'GET'])
def manage_single_person(person_id):
    body = request.get_json() #{ 'username': 'new_username'}
    
    if 'username' not in body:
        raise APIException('You need to specify the username', status_code=400)

    if request.method == 'PUT':
        user1 = Person.query.get(person_id)
        user1.username = body['username']
        db.session.commit()
        return jsonify(user1.serialize()), 200
    if request.method == 'GET':
        user1 = Person.query.get(person_id)
        return jsonify(user1.serialize()), 200

    return "Invalid Method", 404

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
