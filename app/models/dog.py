from app.extensions import db
from app.models.pet import Pet

class Dog(Pet):
    __tablename__ = 'dogs'
    __mapper_args__ = {
        "concrete": True,
    }
    
    id = db.Column(db.Integer, db.ForeignKey('pets.id'), primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=db.func.now())
