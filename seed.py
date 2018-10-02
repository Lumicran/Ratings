"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Rating
from model import Movie
from datetime import datetime

from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print("Movies")

    # Delete all rows in table to streamline second upload.
    Movie.query.delete()

    # Read u.item file (movie data) and parse information.

    for movie in open("seed_data/u.item"):
        movie = movie.rstrip()
        movie = movie.split("|")

        #movie_id = movie[0]
        title = movie[1][:-6]
        released_at = datetime.strptime(str(movie[2]), "%d-%b-%Y")
        print(title)
        imdb_URL = movie[4]

        movie = Movie(#movie_id = movie_id,
                        title = title,
                        released_at = released_at,
                        imdb_url = imdb_URL)

        # Add movie to session
        db.session.add(movie)

    # Commit to push to database
    db.session.commit()


# user_id \t movie_id \t score \t timestamp.
def load_ratings():
    """Load ratings from u.data into database."""

    print("Ratings")

    # Delete all rows in table to steamline second upload.
    Rating.query.delete()

    # Read u.data file (rating data) and parse information.

    for rating in open("seed_data/u.data"):
        rating = rating.rstrip()
        rating = rating.split("\t")

        movie_id = rating[1]
        user_id = rating[0]
        score = rating[2]

        rating = Rating(movie_id= movie_id,
                        user_id= user_id,
                        score= score)

        # Add rating to session
        db.session.add(rating)

    # Commit to push to database
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
