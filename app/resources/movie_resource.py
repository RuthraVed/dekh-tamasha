"""
This is module supports all the REST actions for querying movie data/details.
"""


from sqlalchemy import func
from app_config import db
from models import Movie, Genre


# Python Objects To JSON
def serialize_list(movies_obj_list):
    movies_list = []
    for movie_obj in movies_obj_list:
        movie_dict = {}
        movie_dict["99popularity"] = movie_obj.popularity_factor
        movie_dict["director"] = movie_obj.director
        movie_dict["genre"] = [
            genre_obj.genre_type for genre_obj in movie_obj.movie_genres
        ]
        movie_dict["imdbScore"] = movie_obj.imdb_score
        movie_dict["name"] = movie_obj.name
        movies_list.append(movie_dict)
    return movies_list


# JSON To Python Objects & Save to DB
def db_add(movie_json):
    movie_obj = Movie(
        popularity_factor=movie_json.get("99popularity"),
        director=movie_json.get("director"),
        imdb_score=movie_json.get("imdbScore"),
        name=movie_json.get("name")
    )
    # Adding genres in a way to preserve Many to Many relation
    # class Movie:Parent & class Genre:Child
    genre_list = movie_json.get("genre")
    for g_type in genre_list:
        # Making a pre-check to ensure existing genres are not added again
        genre_type = Genre.query.filter_by(genre_type=g_type).first()
        if genre_type is not None:
            movie_obj.movie_genres.append(genre_type)
        else:
            movie_obj.movie_genres.append(Genre(genre_type=g_type))

    db.session.add(movie_obj)
    db.session.commit()


def get_all(_limit=None):
    movies_obj_list = Movie.query.order_by(Movie.id).limit(_limit).all()
    return serialize_list(movies_obj_list)


def add_movie(movie_json):
    db_add(movie_json)
    last_id = db.session.query(func.max(Movie.id)).scalar()
    movie_obj = db.session.query(Movie).get(last_id)
    return serialize_list([movie_obj])[0]  # It will have only one movie
