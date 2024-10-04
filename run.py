from app import create_app
import pandas as pd
import sys
from app.models.sitter import Sitter
from app.models.review import Review
from app.helpers.csv_handler import CsvHandler

from app.extensions import db

def create_db():
    """
    Drops the current db and recreates it.
    """
    db.drop_all()
    db.create_all()


def bulk_update(entity_df, entity_class):
    """
    Bulk updates entities in the database from a DataFrame.

    Args:
        entity_df (DataFrame): The DataFrame containing entity data to be updated.
        entity_class (class): The ORM class representing the database table.

    This function drops duplicate rows from the given DataFrame, converts it to a list of dictionaries,
    and then performs a bulk update in the database using the `bulk_update` method of the `entity_class`.
    """
    unique_entity_df = entity_df.drop_duplicates()
    unique_entity_list = unique_entity_df.to_dict(orient='records')
    entity_class.bulk_update(db.session, unique_entity_list)

def parse_csv(csv_path):
    """
    Parses a CSV file and commits its data to the database.

    Args:
        csv_path (str): The path to the CSV file.

    This function creates an instance of `CsvHandler` and calls its
    `parse_and_commit_data` method to handle the parsing and committing process.
    """
    csv_handler = CsvHandler(csv_path, db.session)
    csv_handler.parse_and_commit_data()

def update_sitter_info():
    """
    Updates sitter information in the database with review statistics.

    This function queries review statistics per sitter, renames columns for consistency,
    and uses `bulk_update` to update each sitter with their respective sum and count of reviews.
    The session is then committed to save the updates.
    """
    sitter_review_df = pd.read_sql(Review.get_reviews_per_reviewee(db.session).statement, con=db.session.get_bind())
    sitter_review_df = sitter_review_df.rename(columns={'reviewee': 'id'})
    bulk_update(sitter_review_df, Sitter)
    db.session.commit()

def calculate_search_scores():
    """
    Calculates and returns sitter search scores as a DataFrame.

    This function retrieves search score data for all sitters by calling the
    `calculate_all_search_scores` method of the `Sitter` class using the database session.
    It then converts the retrieved data into a pandas DataFrame and returns it.

    Returns:
        DataFrame: A DataFrame containing the search scores and other relevant data for sitters.
    """
    sitter_data = Sitter.calculate_all_search_scores(db.session)
    return pd.DataFrame(sitter_data)

def output_csv():
    """
    Outputs sitter search scores to a CSV file.

    This function calls calculate_search_scores to get a DataFrame of sitter data,
    formats and sorts the DataFrame, and outputs it to a CSV file named 'sitter_scores.csv'.
    """
    output_df = calculate_search_scores()
    output_df = output_df[["email", "name", "profile_score", "ratings_score", "search_score"]]
    output_df.sort_values(by=['search_score', 'name'], ascending=[False, True], inplace=True)
    output_df.to_csv('sitter_scores.csv', index=False, float_format='%.2f')

if __name__ == '__main__':
    """
    Main entry point of the script.

    This section initializes the application context, creates the database,
    parses a CSV file to populate the database, updates sitter information
    with review statistics, and outputs sitter search scores to a CSV file.
    """
    app = create_app()
    with app.app_context():
        create_db()
        parse_csv(sys.argv[1])
        update_sitter_info()
        output_csv()
