from app.extensions import db

class Pet(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=db.func.now())
    