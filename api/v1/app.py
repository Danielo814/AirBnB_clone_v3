#!/usr/bin/python3
"""
creates a new Flask instance
"""
from flask import Flask
from flask import make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=True)
app.url_map.strict_slashes = False

bnbhost = os.getenv('HBNB_API_HOST', default='0.0.0.0')
bnbport = os.getenv('HBNB_API_PORT', default='5000')


@app.teardown_appcontext
def teardown_app(self):
    """
    teardown by closing storage
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """
    error message with invalid endpoint
    """
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    app.run(host=bnbhost, port=int(bnbport), threaded=True)
