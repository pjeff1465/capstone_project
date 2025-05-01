from app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.String(200))
    label = db.Column(db.String(200))
    image = db.Column(db.String(500))
    url = db.Column(db.String(500))
    calories = db.Column(db.Float)
    servings = db.Column(db.Integer)

    user = db.relationship('User', backref='saved_recipes')