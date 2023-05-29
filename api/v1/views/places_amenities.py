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
