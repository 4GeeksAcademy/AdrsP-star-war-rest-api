from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(120), unique=True, nullable = False)
    password = db.Column(db.String(120), unique=False, nullable= False)
    email = db.Column(db.String(120), unique=True, nullable= False)
    favorites = db.relationship("Favorites")

    def __repr__(self):                        # la funcion repr dentro de la clase User le permite regresar la representacion grafica
        return '<User %r>' % self.userName      # de la estructura de tabla que estamos construyendo
    
    def serialize(self):                         # el serialize se encarga de darle una estructura tipo objeto a los datos que ingresamos tipo base de datos de sql alchemy
        return {                                 # ambas funciones (repr y serialize usan de argunmento self porque estan dentro del class User)
            "id": self.id,                      # y asi toman la informacion definida dentro de la funcion 
            "email": self.email,                # ambas funciones se deben definir para cada clase creada
            "userName": self.userName, 
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable = False)
    rotation_period = db.Column(db.Integer, unique=False)
    orbital_period = db.Column(db.Integer, unique=False)
    diameter = db.Column(db.Integer, unique=False)
    climate = db.Column(db.String(120), unique=False)
    gravity = db.Column(db.String(120), unique=False)
    surface_water = db.Column(db.Integer, unique=False)
    population = db.Column(db.Integer, unique=False)
    favorites = db.relationship("Favorites")

    def __repr__(self):
        return '<Planet %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period" : self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter" : self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "surface_water": self.surface_water,
            "population": self.population, 
        }

class Character(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique=False, nullable = False)
    height = db.Column(db.Integer, unique=False)
    mass = db.Column(db.Integer, unique=False)
    hair_color = db.Column(db.String(120), unique=False)
    skin_color = db.Column(db.String(120), unique=False)
    eye_color = db.Column(db.String(120), unique=False)
    birth_year = db.Column(db.String(120), unique=False)
    homeWorld = db.Column(db.String(120), unique=False)
    favorites = db.relationship("Favorites")

    def __repr__(self):
        return '<Character %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "homeWorld": self.homeWorld,
        }


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    planets_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # Add the back_populates attribute             # se debe establecer el backpopulates para la relacion entre ellos
    planet = db.relationship("Planet", back_populates="favorites")
    character = db.relationship("Character", back_populates="favorites")
    user = db.relationship("User", back_populates="favorites")

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planets_id": self.planets_id,
            "character_id": self.character_id,
            "user_id": self.user_id
        }
    