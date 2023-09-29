from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    # Define the one-to-one relationship with the Favorites table
    favorite = db.relationship("Favorites", backref="user", uselist=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        # Serialize the User object, including the favorite character and planet
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "favorite": self.favorite.serialize() if self.favorite else None,
            # do not serialize the password, it's a security breach
        }

class Favorites(db.Model):
    __tablename__ = "Favorites"
    id = db.Column(db.Integer, primary_key=True)
    favorite_character_id = db.Column(db.Integer, db.ForeignKey("Character.id"))
    favorite_planet_id = db.Column(db.Integer, db.ForeignKey("Planet.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))

    # Define the relationships with the Character and Planet tables
    favorite_character = db.relationship("Character", foreign_keys=[favorite_character_id])
    favorite_planet = db.relationship("Planet", foreign_keys=[favorite_planet_id])

    def serialize(self):
        # Serialize the Favorites object, including character and planet details
        return {
            "id": self.id,
            "favorite_character": self.favorite_character.serialize() if self.favorite_character else None,
            "favorite_planet": self.favorite_planet.serialize() if self.favorite_planet else None,
            # You can add more fields here if needed
        }

class Character(db.Model):
    __tablename__ = "Character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(400))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class Planet(db.Model):
    __tablename__ = "Planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(400))
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
