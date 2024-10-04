from abc import abstractmethod
from functools import partialmethod
import logging
from sqlalchemy import insert, update
from sqlalchemy.orm import DeclarativeBase
from app.extensions import db
# 1. Configure logging to output raw SQL statements
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# Declarative base class
class Base(DeclarativeBase):
    metadata = db.metadata  # Associate with the SQLAlchemy metadata

    # Common cols passed down to all models
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=db.func.now())

    @classmethod
    def bulk_add(cls, session, data, sorted=False):
        if not data:
            return []
        ids = session.scalars(
            insert(cls).returning(cls.id, sort_by_parameter_order=sorted), data
        ).all()

        return ids

    @classmethod
    def bulk_update(cls, session, data, sorted=False):
        if not data:
            return []
        session.execute(
            update(cls), data
        ).all()
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    def to_dict(self):
        """
        Converts an instance of a class into a dictionary,
        where keys are attribute names and values are attribute values.
        """
        # Use vars() to dynamically access instance attributes
        # vars(self) returns the instance’s __dict__ (i.e., attribute names and their values)
        return {key: value for key, value in vars(self).items() if not key.startswith('_')}

    @classmethod
    def get_all_as_dicts(cls, session):
        all_rows = cls.get_all(session)
        output = []  # Initialize as a list
        for row in all_rows:
            output.append(row.to_dict())  # Call to_dict() on each instance
        return output
