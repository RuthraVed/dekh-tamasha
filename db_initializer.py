import os
import json

from app_config import db
from datetime import date
from models import User, Movie, Genre

CURRENT_DIR = os.path.dirname(__file__)
SQLITEDB_PATH = os.path.join(CURRENT_DIR, 'dekh_tamasha.db')


def db_initialize():
    db_remove_old()
    db_add_users()
    db_add_movies()
    print("INFO: Successful DB initialization")


def db_remove_old():
    # Delete database file if it exists currently
    if os.path.exists(SQLITEDB_PATH):
        os.remove(SQLITEDB_PATH)

    # Create the database
    db.create_all()


# ----------------ADDING USERS------------------------------------------
def db_add_users():
    json_file = open(os.path.join(CURRENT_DIR, 'data_files/users.json'))
    USERS = json.load(json_file)
    json_file.close()

    num = 0
    for user in USERS:
        user_obj = User(
            full_name=USERS[num].get("full_name"),
            login_name=USERS[num].get("login_name"),
            email=USERS[num].get("email"),
            password=USERS[num].get("password"),
            access_role=USERS[num].get("access_role")
        )
        db.session.add(user_obj)
        num = num+1

    db.session.commit()
    print("INFO: Users table created.")


# ----------------ADDING MOVIES------------------------------------------
def db_add_movies():
    json_file = open(os.path.join(CURRENT_DIR, 'data_files/imdb_data.json'))
    MOVIES = json.load(json_file)
    json_file.close()

    num = 0
    for movie in MOVIES:
        movie_obj = Movie(
            popularity_factor=MOVIES[num].get("99popularity"),
            director=MOVIES[num].get("director"),
            imdb_score=MOVIES[num].get("imdb_score"),
            name=MOVIES[num].get("name"),
            posted_by_user=(User.query.get(1)).id,
            date_posted=date(2020, 12, 31),
        )
        # Adding genres now
        genre_list = MOVIES[num].get("genre")
        for g_type in genre_list:
            # Making a pre-check to ensure existing genres are not added again
            genre_type = Genre.query.filter_by(genre_type=g_type).first()
            if genre_type is not None:
                movie_obj.movie_genres.append(genre_type)
            else:
                movie_obj.movie_genres.append(Genre(genre_type=g_type))

        db.session.add(movie_obj)
        num = num+1

    db.session.commit()
    print("INFO: Movies table created.")


db_initialize()
