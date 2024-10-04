import pytest
from app.models.sitter import Sitter

@pytest.mark.parametrize(
    "name, expected_unique_letters",
    [
        ("", set()),                                        # Empty name, no characters
        ("123456", set()),                                  # No letters, only numbers
        ("$$%%%", set()),                                   # No letters, only special characters
        ("jack", {'j', 'a', 'c', 'k'}),                     # Lowercase letters
        ("AnNa", {'a', 'n'}),                               # Uppercase and lowercase letters
        ("Jane Doe.123!", {'j', 'a', 'n', 'e', 'd', 'o'}),  # mixed characters
        ("!@A#1B$2C%3", {'a', 'b', 'c'})                    # mixed characters, additional
    ]
)
def test_get_unique_letters(name, expected_unique_letters):
    sitter = Sitter(name=name)
    assert sitter.get_unique_letters() == expected_unique_letters



@pytest.mark.parametrize(
    "name, expected_score",
    [
        ("", 0),                 # Empty name, no characters
        ("123456", 0),           # No letters, only numbers
        ("$$%%%", 0),            # No letters, only special characters
        ("Jack", 0.77),          # 'j', 'a', 'c', 'k'
        ("Anna", 0.38),          # 'a', 'n'
        ("Jane Doe.123!", 1.15), # 'j', 'a', 'n', 'e', 'd', 'o'
        ("!@A#1B$2C%3", 0.58)    # 'a', 'b', 'c'
    ]
)
def test_calculate_profile_score(name, expected_score):
    sitter = Sitter(name=name)
    sitter.calculate_profile_score()
    assert sitter.profile_score == expected_score


@pytest.mark.parametrize(
    "sum_of_reviews, number_of_reviews, expected_score",
    [
        (None, None, 0),        # No sum and no number of reviews
        (None, 1, 0),           # No sum of reviews
        (1, None, 0),           # No number of reviews
        (4, 1, 4),              # One review with a score of 4
        (7, 2, 3.5),            # Two reviews with an average score of 3.5
        (14, 3, 4.67)           # Three reviews with an average score of 4.67
    ]
)
def test_calculate_ratings_score(sum_of_reviews, number_of_reviews, expected_score):
    sitter = Sitter()
    # Assign values
    sitter.sum_of_reviews = sum_of_reviews
    sitter.number_of_reviews = number_of_reviews
    # Perform calculation
    sitter.calculate_ratings_score()
    # Assertion
    assert sitter.ratings_score == expected_score

@pytest.mark.parametrize(
    "name, number_of_reviews, sum_of_reviews, expected_search_score",
    [
        ("", 0, 0, 0),             # No profile score; No ratings score; Search score == 0
        ("Alice", 0, 0, 0.96),     # Profile score = 0.96; No ratings score; Search score == profile score
        ("Bob", 10, 40, 4.0),      # Profile score = 0.38; Ratings score: 40 / 10 = 4.0; Search score === ratings score
        ("Charles", 3, 15, 2.45),  # Profile score = 1.35; Ratings score = 5.0; Search score = ((10-3)*1.35 + 3*5.0)/10 = 2.45
        ("", 5, 10, 1.0)           # Profile score == 0; Ratings score: 10 / 5 = 2.0; Search score = ((10-5)*0 + 5*2.0)/10 = 1.00
    ]
)

def test_calculate_search_score(name, number_of_reviews, sum_of_reviews, expected_search_score):
    sitter = Sitter(name=name, number_of_reviews=number_of_reviews, sum_of_reviews=sum_of_reviews)
    sitter.calculate_search_score()
    assert sitter.search_score == expected_search_score
    


