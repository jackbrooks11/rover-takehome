from app.extensions import db

class Review(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    # In the case that a sitter could also review an owner, reviewer and reviewee cols could point to users table instead, making the relationship
    # more flexible.
    reviewer = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviewee = db.Column(db.Integer, db.ForeignKey('sitters.id'))
    # Attaches a review to a specific stay -- would need reconsideration if reviews could be created outside of this context
    booking = db.Column(db.Integer, db.ForeignKey('bookings.id'), unique=True)
    created_on = db.Column(db.DateTime, default=db.func.now())
