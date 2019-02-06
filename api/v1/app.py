#!/usr/bin/python3
"""
creates a new Flask instance
"""
from flask import Flask
from flask import make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=True)
app.url_map.strict_slashes = False

host = getenv('HBNB_API_HOST', default='0.0.0.0')
port = int(getenv('HBNB_API_PORT', default=5000))


@app.teardown_appcontext
def teardown_app(self):
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
