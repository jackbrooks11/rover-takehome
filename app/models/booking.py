from app.extensions import db
from app.models.base import Base

class Booking(Base):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    sitter_id = db.Column(db.Integer, db.ForeignKey('sitters.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Date/time that sitter confirmed the request
    confirmed_date = db.Column(db.DateTime)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
