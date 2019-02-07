#!/usr/bin/python3
"""Module for Reviews API endpoints"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews/', methods=['GET'],
                 strict_slashes=False)
def display_reviews(place_id):
    """Retrieves the list of all review objects
    of a place
    """
    place = storage.get("Place", place_id)
    reviews_list = []
    reviews = storage.all("Review")
    if place:
        for k, v in reviews.items():
            if v.place_id == str(place_id):
                reviews_list.append(v.to_dict())
        return jsonify(reviews_list)
    else:
        abort(404)


@app_views.route('/places/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def display_review(review_id):
    """Retrieves a review object
    """
    try:
        review_obj = storage.get("Review", place_id)
        return jsonify(review_obj.to_dict())
    except:
        abort(404)


@app_views.route('/reviews/<review_id>/', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object
    """
    try:
        review_obj = storage.get("Review", review_id)
        storage.delete(review_obj)
        storage.save()
        return jsonify({}), 200
    except:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a review object
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    new_dict = request.get_json(silent=True)
    if type(new_dict) is dict:
        if "user_id" not in new_dict.keys():
            return jsonify({"error": "Missing user_id"}), 400
        user = storage.get("User", new_dict["user_id"])
        if user is None:
            abort(404)
        if "text" not in new_dict.keys():
            return jsonify({"error": "Missing text"}), 400
        review = Review(text=new_dict["text"], user_id=new_dict["user_id"],
                        place_id=place_id)
        for k, v in new_dict.items():
            setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict()), 201
    else:
        return jsonify({"error": "Not a JSON"}), 400


@app_views.route('/reviews/<review_id>/', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update a review object
    """
    new_dict = request.get_json(silent=True)
    if type(new_dict) is dict:
        review_obj = storage.get("Review", review_id)
        if review_obj is None:
            abort(404)
        for k, v in new_dict.items():
            if k not in ["id", "user_id", "place_id",
                         "created_at", "updated_at"]:
                setattr(review_obj, k, v)
        review_obj.save()
        return jsonify(review_obj.to_dict()), 200
    else:
        return jsonify({"error": "Not a JSON"}), 400
