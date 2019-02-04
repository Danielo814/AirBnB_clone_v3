#!/usr/bin/python3
"""
creates a new Flask instance
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
host = getenv('HBNB_API_HOST', default='0.0.0.0')
port = int(getenv('HBNB_API_PORT', default=5000))

@app.teardown_appcontext
def teardown_app(self):
    storage.close()


if __name__ == "__main__":
    app.run(host=host, port=port)
