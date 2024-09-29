from app.extensions import db
from app.models.person import Person

class Sitter(Person):
    __tablename__ = 'sitters'
    