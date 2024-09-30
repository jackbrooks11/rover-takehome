from app.extensions import db
from app.models.pet import Pet

class Dog(Pet):
    __tablename__ = 'dogs'
    