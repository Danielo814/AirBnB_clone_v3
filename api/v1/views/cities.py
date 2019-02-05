#!/usr/bin/python3
"""Module for City API endpoints"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def display_cities(state_id):
    """Retrieves the list of all city
    objects of a state"""
    state_cities = storage.get("State", state_id)
    cities_list = []
    if state_cities:
        for obj in state_cities.cities:
            cities_list.append(obj.to_dict())
        return jsonify(cities_list)
    else:
        abort(404)

@app_views.route('/cities/<city_id>', methods=['GET'])
def display_city(city_id):
    """Retrieves a city object
    """ 
    try:
        city_obj = storage.get("City", city_id)
        return jsonify(city_obj.to_dict())
    except:
        abort(404)

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city object
    """
    try:
        city_obj = storage.get("City", city_id)
        storage.delete(city_obj)
        response = jsonify({}), 200
        return response
    except:
        abort(404)

@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    new_dict = request.get_json()
    if type(new_dict) is dict:
        if "name" in new_dict.keys():
            # state = State(name=new_dict["name"])
            city = City(name=new_dict["name"])
            for k, v in new_dict.items():
                setattr(city, "state_id", state_id)
                city.save()
                return jsonify(state.to_dict()), 201
        else:
            response = jsonify({"error": "Missing Name"}), 400
            return response
    else:
            response = jsonify({"error": "Not a JSON"}), 400
            return response

"""
TODO
POST and PUT
"""