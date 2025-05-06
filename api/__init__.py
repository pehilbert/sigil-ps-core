import litellm
import logging
import os
from flask import Flask, request, current_app, json
from flask_cors import CORS
from .util.tiamat_db_functions import init_database
from .util.db_config import Config
from .routes.prompt import prompt_bp
from .routes.feedback import feedback_bp
from .routes.personalization import personalization_bp
from .routes.personas import personas_bp
from .extensions import mysql

def create_app():
    app = Flask(__name__)

    litellm.cache = None

    # Configure the app
    app.config['MYSQL_HOST'] = Config.HOST
    app.config['MYSQL_USER'] = Config.USER
    app.config['MYSQL_PASSWORD'] = Config.PASSWORD
    app.config['MYSQL_DB'] = Config.DATABASE
    app.config['MYSQL_CHARSET'] = Config.CHARSET
    app.config['MYSQL_USE_UNICODE'] = Config.UNICODE

    # Set up logging for the app
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s',  # Log format
        handlers=[
            logging.StreamHandler()
        ]
    )

    app.logger = logging.getLogger(__name__)

    # Initialize extensions
    app.logger.info("Initializing MySQL...")
    mysql.init_app(app)
    app.logger.info("MySQL initialized.")

    app.logger.info("Initializing database...")
    with app.app_context():
        init_database(mysql)
    app.logger.info("Database initialized.")

    app.logger.info("Initializing CORS...")
    CORS(app)
    app.logger.info("CORS initialized.")

    # Register blueprints
    app.register_blueprint(prompt_bp, url_prefix='/api')
    app.register_blueprint(feedback_bp, url_prefix='/api')
    app.register_blueprint(personalization_bp, url_prefix='/api')
    app.register_blueprint(personas_bp, url_prefix='/api')

    # Log request info
    @app.before_request
    def log_request_info():
        current_app.logger.info(f"Request: {request.method} {request.path}")

        if request.query_string:
            current_app.logger.info(f"Query: {request.query_string.decode()}")
        if request.is_json:
            body = request.get_json(silent=True)
            if body:
                pretty_body = json.dumps(body, indent=2)
                current_app.logger.info(f"JSON Body:\n{pretty_body}")

    return app