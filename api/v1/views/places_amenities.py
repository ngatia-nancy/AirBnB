#!/usr/bin/python3
"""
Flask api view for the link between Place objects and Amenity objects
"""


from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_for_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    list_amenities = [list.to_dict() for list in place.amenities]
    return jsonify(list_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_for_place(place_id, amenity_id):
    """Deletes an Amenity object from a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
           strict_slashes=False)
def add_amenity_for_place(place_id, amenity_id):
    """Adds an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    else:
        place.amenities.append(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
