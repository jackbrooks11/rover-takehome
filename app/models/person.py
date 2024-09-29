from app.extensions import db

class Person(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    profile_image = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=db.func.now())
    