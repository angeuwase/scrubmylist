"""
This contains the application factory for creating flask application instances.
Using the application factory allows for the creation of flask applications configured 
for different environments based on the value of the CONFIG_TYPE environment variable
"""

import os
from flask import Flask










def create_app():

    app = Flask(__name__)

    # Configure the flask app instance
    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)

    # Configure celery

    # Register blueprints
    register_blueprints(app)


    return app


### Helper Functions ###
def register_blueprints(app):
    from app.auth import auth_blueprint
    from app.main import main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

