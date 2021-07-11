"""
This is module supports all the REST actions for querying movie data/details.
"""


from flask import make_response, abort
from app_config import db
from models import User, UserSchema


def read_all():
    """
    This function responds to endpoint '/api/users'
    with the detailed list of users

    :return:        json string of list of users
    """

    users = User.query.with_entities(
        User.id,
        User.full_name,
        User.login_name,
        User.email,
        User.access_role
    ).order_by(User.id).all()

    # Serialize the data for the response
    user_schema = UserSchema(many=True)
    data = user_schema.dump(users)
    for d in data:
        print(d)
    return data
