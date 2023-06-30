from flask_login import UserMixin
from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from apps import db, login_manager
from apps.authentication.util import hash_pass


class Users(db.Model, UserMixin):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary(255))  # Change to Binary data type for MySQL

    oauth_github = db.Column(db.String(100), nullable=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'password':
                value = hash_pass(value)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.query.get(id)


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None


class OAuth(OAuthConsumerMixin, db.Model):
    __tablename__ = 'OAuth'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id", ondelete="cascade"), nullable=False)
    user = db.relationship(Users)

class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    MPAA_Rating = db.Column(db.String(255))
    budget = db.Column(db.Integer)
    gross = db.Column(db.Integer)
    release_date = db.Column(db.Date)
    genre = db.Column(db.String(255))
    runtime = db.Column(db.Integer)
    rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer)
    profit = db.Column(db.Integer)

def get_movies():
    movies = Movies.query.all()
    return movies

def get_movie_by_id(movie_id):
    movie = Movies.query.get(movie_id)
    return movie






