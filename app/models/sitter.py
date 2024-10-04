import statistics
from app.extensions import db
from app.models.review import Review
from app.models.user import User

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

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(100))
    image = db.Column(db.String(100))
    number_of_reviews = db.Column(db.Integer)
    sum_of_reviews = db.Column(db.Integer)

    def get_unique_letters(self):
        extract_chars = "".join(filter(lambda x: x.isalpha(), self.name.lower()))
        return set(extract_chars) 

    def calculate_profile_score(self):
        """
        Calculates the profile score based on the number of distinct letters in the `name` attribute.
        
        The profile score is determined by:
        - Converting the `name` to lowercase.
        - Extracting only letters.
        - Calculating the fraction of unique letters out of the total alphabet.
        - Multiplying that fraction by 5.

        """
        if not self.name:
            self.profile_score = 0
        else:
            # Total letters in the English alphabet
            total_alphabet_letters = 26
            # Get string containing all letters in name
            unique_chars = self.get_unique_letters()

            # Calculate the profile score as 5 times the fraction of the English alphabet covered
            profile_score_fraction = len(unique_chars) / total_alphabet_letters
            self.profile_score = round(5 * profile_score_fraction, 2)
    
    def calculate_ratings_score(self):
        """
        Calculates the ratings score, which is the average of the stay ratings.

        """
        if not self.sum_of_reviews or not self.number_of_reviews:
            self.ratings_score = 0
        else:
            self.ratings_score = round((self.sum_of_reviews / self.number_of_reviews), 2)

    def calculate_search_score(self):
        """
        Calculates and returns the search score as a weighted average of the Profile Score and Ratings Score.
        
        The Search Score is:
        - Equivalent to the Profile Score if there are no stays.
        - Equivalent to the Ratings Score if there are 10 or more stays.
        - A weighted average of the Profile Score and Ratings Score otherwise.

        """
        self.calculate_profile_score()
        self.calculate_ratings_score()

        if not self.number_of_reviews:
            self.search_score = self.profile_score
        elif self.number_of_reviews >= 10:
            self.search_score = self.ratings_score
        else:
            # Weighted average calculation
            total_weight = 10
            weight_profile = total_weight - self.number_of_reviews
            weight_ratings = self.number_of_reviews

            search_score = (weight_profile * self.profile_score + weight_ratings * self.ratings_score) / total_weight
            self.search_score = round(search_score, 2)

    @classmethod
    def calculate_all_search_scores(cls, session):
        """
        This class method retrieves all sitters from the database, calculates the search score for each
        sitter using their respective method, and compiles their data into a list of dictionaries.

        Returns:
        list of dict: A list where each dictionary contains the data of a sitter after calculating their search score.

        """
        sitters = cls.get_all(session)
        sitter_data = []
        # Process each sitter to calculate scores and create records
        for sitter in sitters:
            sitter.calculate_search_score()
            # Create a dictionary for each sitter
            sitter_record = sitter.to_dict()
            # Append to the list
            sitter_data.append(sitter_record)

        return sitter_data