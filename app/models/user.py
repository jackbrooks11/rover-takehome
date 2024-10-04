from app.extensions import db
from app.models.base import Base
class User(Base):
    __tablename__ = 'users'

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(100))
    image = db.Column(db.String(100))
    
