"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

#base de datos personas 

people = {
    "count": 82, 
    "next": "https://swapi.dev/api/people/?page=2", 
    "previous": None, 
    "results": [
        {
            "name": "Luke Skywalker", 
            "height": "172", 
            "mass": "77", 
            "hair_color": "blond", 
            "skin_color": "fair", 
            "eye_color": "blue", 
            "birth_year": "19BBY", 
            "gender": "male", 
            "homeworld": "https://swapi.dev/api/planets/1/", 
            "films": [
                "https://swapi.dev/api/films/1/", 
                "https://swapi.dev/api/films/2/", 
                "https://swapi.dev/api/films/3/", 
                "https://swapi.dev/api/films/6/"
            ], 
            "species": [], 
            "vehicles": [
                "https://swapi.dev/api/vehicles/14/", 
                "https://swapi.dev/api/vehicles/30/"
            ], 
            "starships": [
                "https://swapi.dev/api/starships/12/", 
                "https://swapi.dev/api/starships/22/"
            ], 
            "created": "2014-12-09T13:50:51.644000Z", 
            "edited": "2014-12-20T21:17:56.891000Z", 
            "url": "https://swapi.dev/api/people/1/"
        },
    ]
}

# base de datos planetas

planets = {
    "count": 60, 
    "next": "https://swapi.dev/api/planets/?page=2", 
    "previous": None, 
    "results": [
        {
            "name": "Tatooine", 
            "rotation_period": "23", 
            "orbital_period": "304", 
            "diameter": "10465", 
            "climate": "arid", 
            "gravity": "1 standard", 
            "terrain": "desert", 
            "surface_water": "1", 
            "population": "200000", 
            "residents": [
                "https://swapi.dev/api/people/1/", 
                "https://swapi.dev/api/people/2/", 
                "https://swapi.dev/api/people/4/", 
                "https://swapi.dev/api/people/6/", 
                "https://swapi.dev/api/people/7/", 
                "https://swapi.dev/api/people/8/", 
                "https://swapi.dev/api/people/9/", 
                "https://swapi.dev/api/people/11/", 
                "https://swapi.dev/api/people/43/", 
                "https://swapi.dev/api/people/62/"
            ], 
            "films": [
                "https://swapi.dev/api/films/1/", 
                "https://swapi.dev/api/films/3/", 
                "https://swapi.dev/api/films/4/", 
                "https://swapi.dev/api/films/5/", 
                "https://swapi.dev/api/films/6/"
            ], 
            "created": "2014-12-09T13:50:49.641000Z", 
            "edited": "2014-12-20T20:58:18.411000Z", 
            "url": "https://swapi.dev/api/planets/1/"
        },
    ]
}

# base de datos usuarios? 

blog_users = [
    {
    "first_name": "Bob",
    "last_name": "Dylan",
    "email": "bob@dylan.com",
    "password": "asdasdasd"
    },
    {
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@doe.com",
    "password": "xdxdxd"
    },
]

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# mis metodos para personas
# 1 er metodo consigue a todas las personas
@app.route('/people', methods=['GET'])
def get_all_people():
    json_text = jsonify(people)
    return json_text

#2ndo metodo para una persona en especifico

@app.route('/people/<int:people_id>')
def get_person(people_id):
    people_list = people['results']
    person = jsonify(people_list[people_id-1])
    return person

# 3er metodo consigue todos los planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():
    json_text = jsonify(planets)
    return json_text

# 4to metodo consigue un planeta en especifico
@app.route('/planets/<int:planet_id>')
def get_planet(planet_id):
    planets_list = planets['results']
    planet = jsonify(planets_list[planet_id-1])
    return planet

# 5to metodo consigue la lista completa de usuarios del blog
@app.route('/blog-users', methods=['GET'])
def get_all_users():
    json_text = jsonify(blog_users)
    return json_text

# 6to metodo consigue los datos de un usuario
@app.route('/blog-users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user_info = blog_users[user_id-1]
    return jsonify(user_info)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
