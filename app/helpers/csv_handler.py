from datetime import datetime
import pandas as pd
from app.models.user import User
from app.models.sitter import Sitter
from app.models.booking import Booking
from app.models.review import Review
from app.models.pet import Pet
from app.models.dog import Dog

class CsvHandler:
    """
    A class to handle parsing and committing CSV data to a database.

    Attributes:
        df (DataFrame): The main DataFrame containing CSV data.
        db_session: The database session for committing data.
        user_df (DataFrame): DataFrame for user data. Initialized as None.
        sitter_df (DataFrame): DataFrame for sitter data. Initialized as None.
        booking_df (DataFrame): DataFrame for booking data. Initialized as None.
        review_df (DataFrame): DataFrame for review data. Initialized as None.
        pet_df (DataFrame): DataFrame for pet data. Initialized as None.
        dog_df (DataFrame): DataFrame for dog data. Initialized as None.
    """

    def __init__(self, csv_path, db_session):
        """
        Initializes CsvHandler with a CSV file path and a database session.

        Args:
            csv_path (str): The path to the CSV file.
            db_session: The database session to use for committing data.
        """
        self.df = pd.read_csv(csv_path)
        self.db_session = db_session
        self.user_df = None
        self.sitter_df = None
        self.booking_df = None
        self.review_df = None
        self.pet_df = None
        self.dog_df = None

    def parse_and_commit_data(self):
        """
        Parses CSV data and commits it to the database.
        """
        self._prepare_user_df()
        self._prepare_sitter_df()
        self._prepare_booking_df()
        self._prepare_review_df()
        self._prepare_pet_df()
        self._prepare_dog_df()
        
        self.db_session.commit()

    def _extract_user_data(self):
        """
        Extracts and combines user data for owners and sitters from the main DataFrame.

        Returns:
            DataFrame: A DataFrame containing user data with unified column names.
        """
        return pd.concat([
            self.df[['owner_email', 'owner', 'owner_phone_number', 'owner_image']].rename(columns=lambda x: x.replace('owner_', '').replace('owner', 'name')),
            self.df[['sitter_email', 'sitter', 'sitter_phone_number', 'sitter_image']].rename(columns=lambda x: x.replace('sitter_', '').replace('sitter', 'name'))
        ])

    def _extract_sitter_data(self):
        """
        Extracts sitter data from the main DataFrame and merges it with user identifiers.

        Returns:
            DataFrame: A DataFrame containing sitter data merged with user IDs.
        """
        sitter_df = self.df[['sitter_email', 'sitter', 'sitter_phone_number', 'sitter_image']]
        sitter_df = sitter_df.merge(self.user_df[['email', 'id']], left_on='sitter_email', right_on='email', how='left').rename(columns=lambda x: x.replace('sitter_', '').replace('sitter', 'name'))
        return sitter_df
    
    def _extract_booking_data(self):
        """
        Extracts booking data from the main DataFrame and includes owner and sitter IDs.

        Returns:
            DataFrame: A DataFrame containing booking data with owner and sitter IDs, including date conversions.
        """
        booking_df = self.df[['rating', 'text', 'sitter_email', 'owner_email', 'response_time_minutes', 'start_date', 'end_date']]
        booking_df.set_index(['sitter_email', 'owner_email', 'start_date', 'end_date'])
        
        # Get owner id for booking dataframe
        booking_df = booking_df.merge(self.user_df[['email', 'id']], left_on='owner_email', right_on='email', how='left').drop(columns=['email', 'owner_email'])
        booking_df = booking_df.rename(columns={'id': 'owner_id'})

        # Get sitter id for booking dataframe
        booking_df = booking_df.merge(self.user_df[['email', 'id']], left_on='sitter_email', right_on='email', how='left').drop(columns=['email', 'sitter_email'])
        booking_df = booking_df.rename(columns={'id': 'sitter_id'})

        booking_df['start_date'] = pd.to_datetime(booking_df['start_date'])
        booking_df['end_date'] = pd.to_datetime(booking_df['end_date'])
        # Add response_time_minutes to current time to get time the sitter confirmed the request
        booking_df['confirmed_date'] = (datetime.now() + pd.to_timedelta(booking_df['response_time_minutes'], unit='m')).apply(lambda x: x.to_pydatetime())

        return booking_df

    def _extract_review_data(self):
        """
        Extracts review data from the booking DataFrame.

        Returns:
            DataFrame: A DataFrame containing review data.
        """
        review_df = self.booking_df
        review_df = review_df.rename(
            columns={
                'owner_id': 'reviewer',
                'sitter_id': 'reviewee',
                'id': 'booking_id',
                'text': 'description'
            }
        )
        return review_df

    def _extract_pet_data(self):
        """
        Extracts pet data from the main DataFrame.

        Returns:
            DataFrame: A DataFrame containing processed pet data with owner ID included.
        """
        pet_df = self.df[['dogs', 'owner_email']]
        # Transforms dog values from pipe-delimited strings to lists
        pet_df['dogs'] = pet_df['dogs'].apply(lambda x: x.split('|'))
        # Creates a new row for each dog
        pet_df = pet_df.explode('dogs').reset_index(drop=True)
        # Merge with user dataframe to get user ids
        pet_df = pet_df.merge(self.user_df[['email', 'id']], left_on='owner_email', right_on='email', how='left').drop(columns=['email', 'owner_email'])

        pet_df = pet_df.rename(columns={'id': 'owner_id', 'dogs': 'name'})
        return pet_df
    
    def _prepare_user_df(self):
        """
        Prepares and inserts user data into the database.

        This method extracts user data from the main DataFrame,
        uses the `_bulk_add` method to insert it into the database,
        and assigns the result to `self.user_df`.
        """
        user_data = self._extract_user_data()
        self.user_df = self._bulk_add(user_data, User)

    def _prepare_sitter_df(self):
        """
        Prepares and inserts sitter data into the database.

        This method extracts sitter data from the main DataFrame,
        uses the `_bulk_add` method to insert it into the database,
        and assigns the result to `self.sitter_df`.
        """
        sitter_df = self._extract_sitter_data()
        self.sitter_df = self._bulk_add(sitter_df, Sitter)

    def _prepare_booking_df(self):
        """
        Prepares and inserts booking data into the database.

        This method extracts booking data from the main DataFrame,
        uses the `_bulk_add` method to insert it into the database,
        and assigns the result to `self.booking_df`.
        """
        booking_df = self._extract_booking_data()
        self.booking_df = self._bulk_add(booking_df, Booking)

    def _prepare_review_df(self):
        """
        Prepares and inserts review data into the database.

        This method extracts review data, uses the `_bulk_add`
        method to insert it into the database, and assigns the
        result to `self.review_df`.
        """
        review_df = self._extract_review_data()
        self.review_df = self._bulk_add(review_df, Review)
    
    def _prepare_pet_df(self):
        """
        Prepares and inserts pet data into the database.

        This method extracts pet data from the main DataFrame,
        uses the `_bulk_add` method to insert it into the database,
        and assigns the result to `self.pet_df`.
        """
        pet_df = self._extract_pet_data()
        self.pet_df = self._bulk_add(pet_df, Pet)

    def _prepare_dog_df(self):
        """
        Prepares and inserts dog data into the database.

        This method directly uses `self.pet_df` as dog data,
        utilizes the `_bulk_add` method to insert it into the
        database, and assigns the result to `self.dog_df`.
        """
        dog_df = self.pet_df
        self.dog_df = self._bulk_add(dog_df, Dog)
    
    def _bulk_add(self, entity_df, entity_class):
        """
        Bulk adds entities to the database from a DataFrame.

        Args:
            entity_df (DataFrame): The DataFrame containing entity data to be inserted.
            entity_class (class): The ORM class representing the database table.

        Returns:
            DataFrame: A DataFrame with records that have been assigned database IDs after insertion.
        
        This method drops duplicate records, converts the DataFrame to a list of dictionaries,
        and uses the `bulk_add` method of the `entity_class` to insert the records and retrieve
        their assigned database IDs. It then adds these IDs back to the records and returns
        them as a DataFrame.
        """
        entity_df = entity_df.drop_duplicates()
        records = entity_df.to_dict(orient='records')
        ids = entity_class.bulk_add(self.db_session, records)
        
        for id, entity_dict in zip(ids, records):
            entity_dict["id"] = id
            
        return pd.DataFrame(records)