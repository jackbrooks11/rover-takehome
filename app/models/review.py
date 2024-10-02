from sqlalchemy import UniqueConstraint
from app.extensions import db
from app.models.base import Base
class Review(Base):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    # To support case where sitter can also review an owner, reviewer and reviewee cols both point to users table.
    reviewer = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviewee = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Attaches a review to a specific stay -- would need reconsideration if reviews could be created outside of this context
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'))
    created_on = db.Column(db.DateTime, default=db.func.now())
    
    __table_args__ = (
        UniqueConstraint('booking_id', 'reviewer', 'reviewee', name='unique_review_constraint'),
    )