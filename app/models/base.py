from abc import abstractmethod
import logging
from sqlalchemy import insert
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
        )
        return ids