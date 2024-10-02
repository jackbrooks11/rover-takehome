from app.extensions import db
from app.models.base import Base
class Pet(Base):
    __tablename__ = 'pets'
    # See comment in sitter.py for explanation of why this config using joined table inheritance
    # is not being used.
    #
    # __mapper_args__ = {
    #     'polymorphic_identity': 'pet',
    #     'polymorphic_on': 'type'
    # }
    # type = db.Column(db.String(50))
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=db.func.now())
    