#!/usr/bin/python3
"""
users module containing methods for retreiving
and updating user objects
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET'], strict_slashes=False)
def display_users():
    """Retrieves the list of all user objects
    """
    users = storage.all("User").values()
    users_list = []
    for obj in users:
        users_list.append(obj.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>/', methods=['GET'], strict_slashes=False)
def display_user(user_id=""):
    """Retrieves a user object
    """
    try:
        user_obj = storage.get("User", user_id)
        return jsonify(user_obj.to_dict())
    except:
        abort(404)


@app_views.route('/users/<user_id>/', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Retrieves a user object
    """
    try:
        user_obj = storage.get("User", user_id)
        storage.delete(user_obj)
        storage.save()
        return jsonify({}), 200
    except:
        abort(404)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a user object
    """
    new_dict = request.get_json()
    if type(new_dict) is dict:
        if "email" not in new_dict.keys():
            return jsonify({"error": "Missing email"}), 400
        elif "password" not in new_dict.keys():
            return jsonify({"error": "Missing password"}), 400
        else:
            user = User(email=new_dict["email"], password=new_dict["password"])
            for k, v in new_dict.items():
                setattr(user, k, v)
            user.save()
            return jsonify(user.to_dict()), 201
    else:
            return jsonify({"error": "Not a JSON"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a user object
    """
    new_dict = request.get_json()
    if type(new_dict) is dict:
        user_obj = storage.get("User", user_id)
        if user_obj is None:
            abort(404)
        for k, v in new_dict.items():
            if k not in ["id", "email", "created_at", "updated_at"]:
                setattr(user_obj, k, v)
        user_obj.save()
        return jsonify(user_obj.to_dict()), 200
    else:
        response = jsonify({"error": "Not a JSON"}), 400
        return response
