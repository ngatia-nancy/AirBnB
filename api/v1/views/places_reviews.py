#!/usr/bin/python3
"""
Flask api for review views
"""


from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """Retrieves the list of all review objects of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    list_reviews = [review.to_dict() for review in place.reviews]
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object by its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object by its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new review object for a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}))
    if 'user_id' not in data:
        return make_response(jsonify({'error': 'Missing user_id'}))
    if 'text' not in data:
        return make_response(jsonify({'error': 'Missing text'}))
    data['place_id'] = place_id
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    new_review = Review(**data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 200)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a review object by its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}))
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
