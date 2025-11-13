from flask import Flask, current_app, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .config import Config

from .db.connection import Database

import os

jwt = JWTManager()


def create_app() -> Flask:

    app = Flask(__name__, static_folder="static", template_folder="templates")  

    NUXT_DIST_DIR = os.path.join(os.path.dirname(__file__), "static")  
    NUXT_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "static", "_nuxt")

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
    
    @app.route('/_nuxt/<path:filename>')
    def nuxt_static(filename):
        return send_from_directory(NUXT_ASSETS_DIR, filename)
    
    @app.route("/images/<path:filename>")
    def nuxt_images(filename):
        return send_from_directory(os.path.join(NUXT_DIST_DIR, "images"), filename)

    @app.route("/_ipx/<path:path>")
    def ipx_passthrough(path):
        """
        Redirects Nuxt Image IPX optimization URLs (e.g., /_ipx/s_96x96/images/noAvatar.jpg)
        to serve actual static images.
        """
        # Example path: "_/images/noAvatar.jpg" → we need everything after "images/"
        parts = path.split("/images/", 1)
        if len(parts) == 2:
            filename = parts[1]
            return send_from_directory(os.path.join(NUXT_DIST_DIR, "images"), filename)

        return jsonify({"error": "Invalid IPX path"}), 404
    
    @app.route('/favicon.svg')
    def favicon_svg():
        return send_from_directory(NUXT_DIST_DIR, 'favicon.svg')

    # Serve index.html for any non-API route
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        # Prevent catching API routes
        if path.startswith("api/"):
            return jsonify({"error": "Not Found"}), 404
        return render_template('index.html')

    return app
