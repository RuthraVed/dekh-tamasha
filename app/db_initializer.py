import os
import json

from app_config import db
from datetime import date
from models import User, Movie, Genre

CURRENT_DIR = os.path.dirname(__file__)
sqliteDB_file_path = os.path.join(CURRENT_DIR, 'dekh_tamasha.db')

# Delete database file if it exists currently
if os.path.exists(sqliteDB_file_path):
    os.remove(sqliteDB_file_path)


# Create the database
db.create_all()


# ----------------ADDING USERS------------------------------------------
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
print("SUCCESS: Users table created.")


# ----------------ADDING MOVIES------------------------------------------
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
print("SUCCESS: Movies table created.")

# To Query object with specific columns-------------
# user_obj = User.query.with_entities(
#     User.id.label('userId'),
#     User.full_name.label("firstName"),
#     User.login_name.label("loginName"),
#     User.email,
#     User.access_role.label("accessRole")
# ).order_by(User.id).first()

# print(user_obj.firstName)
