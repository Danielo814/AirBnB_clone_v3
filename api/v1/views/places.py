#!/usr/bin/python3
"""Module for Places API endpoints"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def display_places(city_id):
    """Retrieves the list of all places
    objects of a city"""
    city = storage.get("City", city_id)
    places_list = []
    places = storage.all("Place")
    if city:
        for key, value in places.items():
            if value.city_id == str(city_id):
                places_list.append(value.to_dict())
        return jsonify(places_list)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'])
def display_place(place_id):
    """Retrieves a place object
    """
    try:
        place_obj = storage.get("Place", place_id)
        return jsonify(place_obj.to_dict())
    except:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a place object
    """
    try:
        place_obj = storage.get("Place", place_id)
        storage.delete(place_obj)
        storage.save()
        response = jsonify({}), 200
        return response
    except:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
    creates a new place
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    new_dict = request.get_json()
    if type(new_dict) is dict:
        if "user_id" not in new_dict.keys():
            return jsonify({"error": "Missing user_id"}), 400
        user = storage.get("User", new_dict["user_id"])
        if user is None:
            abort(404)
        if "name" not in new_dict.keys():
            return jsonify({"error": "Missing name"}), 400
        place = Place(name=new_dict["name"], user_id=new_dict["user_id"],
                      city_id=city_id)
        for k, v in new_dict.items():
            setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict()), 201
    else:
            response = jsonify({"error": "Not a JSON"}), 400
            return response


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """updates a place object
    """
    new_dict = request.get_json()
    if type(new_dict) is dict:
        place_obj = storage.get("Place", place_id)
        if place_obj is None:
            abort(404)
        for k, v in new_dict.items():
            if k not in ["id", "user_id", "city_id",
                         "created_at", "updated_at"]:
                setattr(place_obj, k, v)
        place_obj.save()
        return jsonify(place_obj.to_dict()), 200
    else:
        response = jsonify({"error": "Not a JSON"}), 400
        return response
