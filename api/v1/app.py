#!/usr/bin/python3
"""
starts a Flask web application API
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def shutdown_session(exception=None):
    """closes the session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handles 404 error"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = int(getenv('HBNB_API_PORT', default='5000'))
    app.run(host='0.0.0.0', port='5000', threaded=True)
