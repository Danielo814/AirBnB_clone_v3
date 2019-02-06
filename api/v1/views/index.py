#!/usr/bin/python3
"""Index views"""

from api.v1.views import app_views
from flask import jsonify, Flask
from models import storage


@app_views.route('/status')
def display_status():
    """status page
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def display_stats():
    """retrieves the number of
    each objects by type"""
    result = {}
    cls_dict = {"Amenity": "amenities", "City": "cities", "Place": "places",
                "Review": "reviews", "State": "states", "User": "users"}

    for k, v in cls_dict.items():
        result[v] = storage.count(k)
    return jsonify(result)
