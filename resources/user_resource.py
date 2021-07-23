"""
This is module supports all the REST actions for querying movie data/details.
"""
from app_config import db
from models import User


# Python Objects To JSON
def serialize_list(users_obj_list):
    users_list = []
    for user_obj in users_obj_list:
        user_dict = {}
        user_dict["firstName"] = user_obj.full_name
        user_dict["userName"] = user_obj.login_name
        user_dict["emailId"] = user_obj.email
        user_dict["accessLevel"] = user_obj.access_role
        users_list.append(user_dict)
    return users_list


def get_all(_limit=None):
    users_obj_list = db.session.query(
        User).order_by(User.id).limit(_limit).all()
    return serialize_list(users_obj_list)


def basic_auth(username, password, required_scopes=None):
    user = User.query.filter(User.login_name == username).one_or_none()
    if user is not None:
        if user.password == password:
            return {'sub': 'admin'}
    return {"message": "User authentication failed."}, 401
