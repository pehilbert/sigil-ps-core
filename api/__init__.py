import litellm
from flask import Flask
from flask_cors import CORS
from .util.db_config import Config
from .routes.prompt import prompt_bp
from .routes.feedback import feedback_bp
from .routes.personalization import personalization_bp
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

    # Initialize extensions
    mysql.init_app(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(prompt_bp, url_prefix='/api')
    app.register_blueprint(feedback_bp, url_prefix='/api')
    app.register_blueprint(personalization_bp, url_prefix='/api')

    return app