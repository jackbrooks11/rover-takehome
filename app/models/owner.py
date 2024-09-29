from app.extensions import db
from app.models.person import Person

class Owner(Person):
    __tablename__ = 'owners'

    