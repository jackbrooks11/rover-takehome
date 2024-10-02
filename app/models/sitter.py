from app.extensions import db
from app.models.user import User
from app.utils import extract_characters

class Sitter(User):
    __tablename__ = 'sitters'
    # Using concrete inheritance rather than joined table inheritance for two main reasons:
    #   1. When running search score algorithm, don't need to join to User table to get Sitter info
    #   2. Bulk insert on this table will not break down to single inserts. In joined table inheritance
    #      where the primary key of this table would be a foreign key to users.id, the default sqlalchemy
    #      behavior is to first insert a row into User, fetch the inserted id, and then insert into Sitter
    # Joined table inheritance would reduce data redundancy by not requiring us to re-define columns in
    # Sitter. If bulk load of csv was not required, this would probably be the way to go.
    __mapper_args__ = {
        "concrete": True,
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(100))
    profile_image = db.Column(db.String(100))