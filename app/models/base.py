from sqlalchemy import insert, update
from sqlalchemy.orm import DeclarativeBase
from app.extensions import db

# Declarative base class
class Base(DeclarativeBase):
    metadata = db.metadata  # Associate with the SQLAlchemy metadata

    # Common cols passed down to all models
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=db.func.now())

    @classmethod
    def bulk_add(cls, session, data, sorted=False):
        """
        Performs a bulk addition of records to the database for a specific model.

        Args:
            session: The database session to use for the transaction.
            data (list): A list of dictionaries where each dictionary represents a record.
            sorted (bool): If True, sorts by parameter order, otherwise adds directly.

        Returns:
            list: A list of IDs of the inserted records.
        """
        if not data:
            return []
        ids = session.scalars(
            insert(cls).returning(cls.id, sort_by_parameter_order=sorted), data
        ).all()

        return ids

    @classmethod
    def bulk_update(cls, session, data):
        """
        Performs a bulk update of records in the database for a specific model.

        Args:
            session: The database session to use for the transaction.
            data (list): A list of dictionaries where each dictionary represents updated field values.

        Returns:
            None
        """
        if not data:
            return []
        session.execute(
            update(cls), data
        ).all()
    
    @classmethod
    def get_all(cls, session):
        """
        Retrieves all records from the database for a specific model.

        Args:
            session: The database session to use for the query.

        Returns:
            list: A list of all instances of the model from the database.
        """
        return session.query(cls).all()

    def to_dict(self):
        """
        Converts the instance into a dictionary.

        Returns:
            dict: A dictionary representation of the instance where keys are attribute names
            and values are attribute values, excluding private attributes.
        """
        # Use vars() to dynamically access instance attributes
        # vars(self) returns the instance’s __dict__ (i.e., attribute names and their values)
        return {key: value for key, value in vars(self).items() if not key.startswith('_')}

    @classmethod
    def get_all_as_dicts(cls, session):
        """
        Retrieves all records from the database for a specific model and converts them into dictionaries.

        Args:
            session: The database session to use for the query.

        Returns:
            list: A list of dictionaries, each representing an instance of the model.
        """
        all_rows = cls.get_all(session)
        output = []  # Initialize as a list
        for row in all_rows:
            output.append(row.to_dict())  # Call to_dict() on each instance
        return output
