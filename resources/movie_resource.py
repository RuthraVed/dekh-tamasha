"""
This is module supports all the REST actions for querying movie data/details.
"""
from sqlalchemy import func, desc
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


def serialize_single(movie_obj):
    movie_dict = {}
    movie_dict["movieId"] = movie_obj.id
    movie_dict["99popularity"] = movie_obj.popularity_factor
    movie_dict["director"] = movie_obj.director
    movie_dict["genre"] = [
        genre_obj.genre_type for genre_obj in movie_obj.movie_genres
    ]
    movie_dict["imdbScore"] = movie_obj.imdb_score
    movie_dict["name"] = movie_obj.name
    return movie_dict


# JSON To Python Objects & Save to DB
def db_add(movie_json, movie_obj=None, movie_id=None):
    if movie_obj is not None:
        movie_obj.popularity_factor = movie_json.get("99popularity")
        movie_obj.director = movie_json.get("director")
        movie_obj.imdb_score = movie_json.get("imdbScore")
        movie_obj.name = movie_json.get("name")
    else:
        # Creating a movie obj
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
    temp_dict = serialize_list([movie_obj])[0]
    movie_name_dict = {}
    movie_name_dict["movieId"] = last_id
    movie_name_dict["movieName"] = temp_dict.get("name", None)
    return movie_name_dict  # It will have only one movie


def get_movie_by_id(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is not None:
        return serialize_list([movie])[0], 200
    return {"message": "Movie not found."}, 404


def edit_by_id(movie_json, movie_id):
    movie_obj = Movie.query.filter(Movie.id == movie_id).one_or_none()
    print(movie_obj)
    if movie_obj is not None:
        db_add(movie_json, movie_obj, movie_id)
        return serialize_list([movie_obj])[0], 200
    return {"message": "Movie not found."}, 404


def delete_by_id(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return {
            "message": f"Movie having Id:{movie_id} deleted.",
        }
    return {"message": "Movie not found."}, 404


def search_by_name(search_name):
    movies_obj_list = db.session.query(Movie).filter(
        Movie.name.like(f'%{search_name}%')).all()
    if movies_obj_list is not None and movies_obj_list != []:
        movies_list = []
        for movie_obj in movies_obj_list:
            movies_list.append(serialize_single(movie_obj))
        return movies_list, 200
    else:
        return {"message": "Movies not found by provided movieName."}, 200


def search_by_director(search_director):
    movies_obj_list = db.session.query(Movie).filter(
        Movie.director.like(f'%{search_director}%')).all()
    if movies_obj_list is not None and movies_obj_list != []:
        movies_list = []
        for movie_obj in movies_obj_list:
            movies_list.append(serialize_single(movie_obj))
        return movies_list, 200
    else:
        return {"message": "Movies not found by provided directorName."}, 200


def get_top_movies_by_popularity(_limit=3):
    movies_obj_list = db.session.query(Movie).order_by(
        desc(Movie.popularity_factor)).limit(_limit).all()
    if movies_obj_list is not None and movies_obj_list != []:
        movies_list = []
        for movie_obj in movies_obj_list:
            movies_list.append(serialize_single(movie_obj))
        return movies_list, 200
    else:
        return {"message": "Movies not found by criteria."}, 200


def get_top_movies_by_imdb(_limit=3):
    movies_obj_list = db.session.query(Movie).order_by(
        desc(Movie.imdb_score)).limit(_limit).all()
    if movies_obj_list is not None and movies_obj_list != []:
        movies_list = []
        for movie_obj in movies_obj_list:
            movies_list.append(serialize_single(movie_obj))
        return movies_list, 200
    else:
        return {"message": "Movies not found by criteria."}, 200
