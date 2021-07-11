from datetime import datetime

from app_config import db, ma


# -------USER MODEL-------------------------
class User(db.Model):
    __tablename__ = "user_profile"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(32), nullable=False)
    login_name = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    access_role = db.Column(db.String(32), nullable=False, default="User")
    posted_movies = db.relationship('Movie', backref='user_profile', lazy=True)


def __repr__(self):
    return f"[{self.id},\t{self.full_name},\t{self.login_name},\t{self.email},\t{self.password},\t{self.access_role}]"


# A helper table for many to many relationship
movie_genre = db.Table('movie_genre',
                       db.Column('genre_id', db.Integer, db.ForeignKey(
                           'genre.id'), primary_key=True),
                       db.Column('movie_id', db.Integer, db.ForeignKey(
                           'movie.id'), primary_key=True)
                       )


# -------MOVIE MODEL-------------------------
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    popularity_factor = db.Column(db.Float, default=00.0)
    director = db.Column(db.String(32), nullable=False)
    # defining the many to many relationship
    movie_genres = db.relationship(
        'Genre', secondary=movie_genre, lazy='subquery', backref=db.backref('movie', lazy=True))
    imdb_score = db.Column(db.Float, default=0.0)
    name = db.Column(db.String(64), nullable=False)
    posted_by_user = db.Column(
        db.Integer, db.ForeignKey('user_profile.id'), nullable=True)
    date_posted = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    def __repr__(self):
        return f"[{self.id},\t{self.popularity_factor},\t{self.name},\t{self.director},\t{self.imdb_score},\t{self.date_posted}]"


# -------GENRE MODEL-------------------------
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre_type = db.Column(db.String(16), unique=True, nullable=False)

    def __repr__(self):
        return f"[{self.id},\t{self.genre_type}]"


# ------------------For serializing the above Model objects-----------------------------------------

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True


class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        include_relationships = True
        load_instance = True


class GenreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        include_relationships = True
        load_instance = True
