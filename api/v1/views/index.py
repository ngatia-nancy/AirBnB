#!/usr/bin/python3
"""
    A route /status on the object app_views that returns a
    status: OK JSON
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def app_status():
    """
         a route /status on the object app_views that returns
         a JSON: "status": "OK"
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def all_stats():
    """
        Create an endpoint that retrieves the number of each objects by type
    """
    obj = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User),
        }
    return jsonify(obj)


if __name__ == "__main__":
    pass
