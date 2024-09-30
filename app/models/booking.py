from app.extensions import db

class Booking(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sitter = db.Column(db.Integer, db.ForeignKey('sitters.id'))
    owner = db.Column(db.Integer, db.ForeignKey('owners.id'))
    request_date = db.Column(db.DateTime,  default=db.func.now(), nullable=False)
    confirmed_date = db.Column(db.DateTime)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
