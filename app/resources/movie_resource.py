"""
This is module supports all the REST actions for querying movie data/details.
"""


from flask import make_response, abort
from app_config import db
from models import Movie, MovieSchema


def read_all():
    """
    This function responds to endpoint '/api/movies'
    with the detailed list of movies

    :return:        json string of list of movies
    """

    movies_obj_list = Movie.query.order_by(Movie.id).all()
    movies_list = []

    for movie_obj in movies_obj_list:
        movie_dict = {}
        movie_dict["99popularity"] = movie_obj.popularity_factor
        movie_dict["director"] = movie_obj.director
        movie_dict["genre"] = [
            genre_obj.genre_type for genre_obj in movies_obj_list[0].movie_genres
        ]
        movie_dict["imdbScore"] = movie_obj.imdb_score
        movie_dict["name"] = movie_obj.name
        movies_list.append(movie_dict)

    return movies_list
