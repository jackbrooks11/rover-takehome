from app.extensions import db
from app.models.user import User

class Sitter(User):
    __tablename__ = 'sitters'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)