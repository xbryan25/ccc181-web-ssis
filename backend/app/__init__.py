from flask import Flask, current_app, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .config import Config

from .db.connection import Database

jwt = JWTManager()


def create_app() -> Flask:

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

    # Override default JWT error messages
    @jwt.unauthorized_loader
    def custom_missing_cookie_callback(err):
        if "text/html" in request.headers.get("Accept", ""):
            # Accessed directly in browser
            return jsonify(error="This page requires login. Please log in via the website."), 401
        else:
            # API / frontend fetch
            return jsonify(error="Authentication required. Please log in first."), 401

    @jwt.invalid_token_loader
    def custom_invalid_token_callback(err):
        return jsonify({"error": "Invalid or expired token. Please log in again."}), 401

    @jwt.expired_token_loader
    def custom_expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Session expired. Please log in again."}), 401

    return app
