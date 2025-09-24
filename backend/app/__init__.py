from flask import Flask, current_app
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .config import Config

from .db.connection import Database

jwt = JWTManager()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    jwt.init_app(app)
    CORS(app, origins=["http://127.0.0.1:3000"], supports_credentials=True)
    
    from .features import student_bp, program_bp, college_bp, user_bp

    app.register_blueprint(student_bp, url_prefix='/api/students')
    app.register_blueprint(program_bp, url_prefix='/api/programs')
    app.register_blueprint(college_bp, url_prefix='/api/colleges')
    app.register_blueprint(user_bp, url_prefix='/api/user')

    with app.app_context():
        current_app.extensions['db'] = Database()

    return app
