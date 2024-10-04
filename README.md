# Rover Take-home Project

## Description

The Rover Take-home Project is an effort to rebuild the search ranking algorithm for Rover.com, a dog sitting service platform that was compromised in an unfortunate accident. Our goal is to recreate the search scores for sitters using data retrieved from the Google search index. This project involves developing a simple command-line program to process, calculate, and output search rankings in CSV format based on specified criteria.
## Table of Contents

1. [Project Structure](#project-structure)

2. [Setup and Installation](#setup-and-installation)

3. [Usage](#usage)

4. [Testing](#testing)

5. [Discussion Question](#discussion-question)

6. [Output](#output)

## Project Structure

The project is organized as follows:

- `app/`: Contains the application code and supporting files.

- `__init__.py`: Initializes the Flask application and its extensions.

- `models/`: Contains ORM models for the data.

- `helpers/`: Includes helper classes, such as `CsvHandler`, to parse and commit data.

- `extensions/`: Initializes any extensions, such as the database.

- `data/`: Data for the project, including an input CSV file with reviews.

- `run.py`: The main script to execute the program logic.

- `config.py`: Configuration settings for the application.

- `requirements.txt`: Python dependencies.

## Setup and Installation

### Prerequisites

- Python 3.x

- pip (Python package manager)

- virtualenv (Optional but recommended for creating a virtual environment)

### Instructions

1. **Clone the repository:**

```bash

git clone https://github.com/jackbrooks11/rover-takehome.git

cd rover-takehome

```

2. **Set up a virtual environment (optional but recommended):**

```bash

python3 -m venv venv

source venv/bin/activate # On Windows, use `venv\Scripts\activate`

```

3. **Install dependencies:**

```bash

pip install -r requirements.txt

```

4. **Configure environment variables (if needed):**
```bash
export FLASK_APP=app

export FLASK_ENV=development
```
## Usage

To run the program, execute the following command:

```bash

python run.py <path-to-csv-file>

```

This will parse the CSV file, process the sitter and review data, compute the search scores, and output the results to `sitter_scores.csv`.

## Testing

To ensure the functionality works as expected, tests have been created. You can run the tests using `pytest`.

```bash
cd tests

python -m pytest
```
## Output

The output CSV, `sitters.csv`, consists of the following columns:

- `email`: The sitter's email.

- `name`: The sitter's name.

- `profile_score`: The calculated profile score.

- `ratings_score`: The calculated ratings score.

- `search_score`: The computed search score used for ranking.

The CSV is sorted by `search_score` in descending order, with ties broken alphabetically by `name`.


## Discussion Question

Imagine you are designing a Rover-like production web application based on the exercise you've just completed. This application will compute the search scores for sitters, generate search results based on those scores, and display them to users through a web UI.

### How would you adjust the calculation and storage of search scores in a production application?

In a production application, I would expect there to be a much more sophisticated search score algorithm than that which we have created for this project. While the Ratings Score (which is the average of the sitter's stay ratings) would still be useful, the Profile Score (5 times the fraction of the English alphabet comprised by the distinct letters of the sitter's name) would not be. Instead, I would replace it with a wide range of parameters to be specified by the user when they execute a search. For example, the sitter's geographical proximity to the user would be taken into account, as well as the services they provide, their rate, availability, etc.

It's clear we want to prioritize quick calculation of search scores to provide a seamless user experience. Therefore, we would not want to calculate search scores from scratch each time a user executes a search. One strategy would be to execute a query that updates a sitter's average stay ratings each time a review is added. Then, we could store these results in a cache/in-memory database for quick lookup.