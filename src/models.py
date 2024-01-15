from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
   # __tablename__="user"

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(120), unique=True, nullable = False)
    password = db.Column(db.String(120), unique=False, nullable= False)
    email = db.Column(db.String(120), unique=True, nullable= False)
    favorites = db.relationship("Favorites")

    def __repr__(self):
        return '<User %r>' % self.userName
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "userName": self.userName, 
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
   # __tablename__="planet"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable = False)
    rotation_period = db.Column(db.Integer, unique=False)
    orbital_period = db.Column(db.Integer, unique=False)
    diameter = db.Column(db.Integer, unique=False)
    climate = db.Column(db.String(120), unique=False)
    gravity = db.Column(db.String(120), unique=False)
    surface_water = db.Column(db.Integer, unique=False)
    population = db.Column(db.Integer, unique=False)
    #Favorites_id=db.Column(db.Integer, db.ForeignKey("favorites.id"))
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
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
   # __tablename__="character"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique=False, nullable = False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=False)
    hair_color = db.Column(db.String(120), unique=False, nullable = False)
    skin_color = db.Column(db.String(120), unique=False, nullable = False)
    eye_color = db.Column(db.String(120), unique=False, nullable = False)
    birth_year = db.Column(db.String(120), unique=False, nullable = False)
    homeWorld = db.Column(db.String(120), unique=False, nullable = False)
    #Favorites_id=db.Column(db.Integer, db.ForeignKey("favorites.id"))
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
            # do not serialize the password, its a security breach
        }


class Favorites(db.Model):
   # __tablename__="favorites"

    id = db.Column(db.Integer, primary_key = True)
    planets_id = db.Column(db.Integer, db.ForeignKey("Planets.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("Character.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planets_id": self.planets_id,
            "character_id": self.character_id,
            "user_id": self.user_id
            # do not serialize the password, its a security breach
        }
    