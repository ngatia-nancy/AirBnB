#!/usr/bin/python3
"""Flask api for place views"""


from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city_id(city_id):
    """Retrieves the list of all place objects of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    list_places = [place.to_dict() for place in city.places]
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves the place object with the given id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places.<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """Deletes the place object with the given id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def add_place_to_city(city_id):
    """Adds a place to the city with the given id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.json:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    data = request.json
    data['city_id'] = city_id
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    new_place = Place(**data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place_by_id(place_id):
    """Updates the place object with the given id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.json()
    for key, value in data.items():
        if key not in ['id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
