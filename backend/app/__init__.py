from flask import Flask
from flask_cors import CORS

from .config import Config


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app, origins='*')
    
    from .features import student_bp, program_bp

    app.register_blueprint(student_bp, url_prefix='/api/students')
    app.register_blueprint(program_bp, url_prefix='/api/programs')

    return app
