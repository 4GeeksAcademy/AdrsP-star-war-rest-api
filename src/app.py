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
from models import db, User, Character, Favorites, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False


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

# get all users

@app.route('/user', methods=['GET'])
def handle_hello():
    user = User.query.all() # trae una lista de objetos de la tabla user
    results = list(map(lambda usuarios : usuarios.serialize(), user)) # se realiza el mapeo y posterior generacion de la lista con los resultados
    
    return jsonify(results), 200

# get one user

@app.route('/user/<int:user_id>', methods=['GET'])
def handle_user(user_id):
    user = User.query.filter_by(id = user_id).first() 
    results = user.serialize()
    
    return jsonify(results), 200

# 1 er metodo consigue a todas las personas / characters
@app.route('/characters', methods=['GET'])
def get_all_people():
    people = Character.query.all()
    results = list(map(lambda character : character.serialize(), people))

    json_text = jsonify(results)
    return json_text, 200

#2ndo metodo para una persona en especifico

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_person(character_id):
    character = Character.query.filter_by(id = character_id).first()
    results = character.serialize()
    return results

# 3er metodo consigue todos los planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planet_list = Planet.query.all()
    results = list(map(lambda planeta : planeta.serialize(), planet_list))
    return results , 200

# 4to metodo consigue un planeta en especifico
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.filter_by(id = planet_id).first()
    results = planet.serialize()
    return results , 200

# lista de favoritos x usuario

@app.route('/user/<int:id_user>/favorites', methods=['GET'])
def get_user_favorites(id_user):
    user_favorites = Favorites.query.filter_by(user_id = id_user)
    results = list(map(lambda favorite: favorite.serialize(), user_favorites))
    return results , 200

# asignar favoritos a un usuario

@app.route('/user/<int:id_user>/favorites', methods=['POST'])
def add_new_todo(id_user):
    data = request.json  # Assuming data is sent in JSON format
    data['user_id'] = str(id_user) # asigno nueva key al diccionario "data" y a esa key le asigno el usuario de la ruta
    new_record = Favorites(**data)

    db.session.add(new_record)
    db.session.commit()

    return jsonify({'message': 'Record created successfully'}), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
