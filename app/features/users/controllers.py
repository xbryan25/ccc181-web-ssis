from flask import request, jsonify, make_response, current_app, Response

from flask_jwt_extended import create_access_token, get_jwt_identity, set_access_cookies, unset_jwt_cookies, create_refresh_token, set_refresh_cookies, unset_refresh_cookies

import traceback

from .services import UserServices

from app.utils import validate_email_format, validate_username_format, validate_password

from app.exceptions.custom_exceptions import ValidationError

from datetime import datetime, timedelta, timezone

import re


class UserController:
 
    @staticmethod
    def user_login_controller() -> tuple[Response, int]:
        """Generate JWT access and refresh tokens, and set them as HTTP-only cookies after validating user credentials."""

        user_login_details = request.json

        try:
            user = UserServices.user_login_service(user_login_details.get('email'), user_login_details.get('password'))
            
            if not user:
                return jsonify({"error": "Invalid credentials."}), 401
            
            access_token = create_access_token(identity=user.user_id)
            refresh_token = create_refresh_token(identity=user.user_id)

            expires_at = (datetime.now(timezone.utc) + timedelta(seconds=current_app.config["COOKIE_MAX_AGE"])).timestamp() * 1000

            resp = make_response({
                "username": user.username,
                "messageTitle": "Login successful.",
                "message": "Enjoy your session!",
                "accessTokenExpiresAt": expires_at
            })
            
            set_access_cookies(resp, access_token, max_age=current_app.config["COOKIE_MAX_AGE"])
            set_refresh_cookies(resp, refresh_token, max_age=current_app.config["REFRESH_COOKIE_MAX_AGE"])

            return resp, 200
        
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def user_logout_controller() -> tuple[Response, int]:
        """Unsets both access and refresh tokens."""

        try:
            resp = make_response({
                "messageTitle": "Logout successful.",
                "message": "Your session has been cleared."
            })

            # Clears both access and refresh cookies
            unset_jwt_cookies(resp)

            return resp, 200
        
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def user_signup_controller() -> tuple[Response, int]:
        """Register a new user using signup details."""

        user_signup_details = request.json

        try:
            validate_email_format(user_signup_details['email'])

            validate_username_format(user_signup_details['username'])

            validate_password(user_signup_details['password'])

            UserServices.validate_signup_details(user_signup_details['email'], user_signup_details['username'])

            UserServices.user_signup_service(user_signup_details)
            
            return jsonify({"messageTitle": "Signup successful.", "message": "Your account is ready. Enjoy using Sequence!"}), 201
        
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": "An unexpected error occurred."}), 500
        
    @staticmethod
    def get_current_user_controller() -> tuple[Response, int]:
        "Retrieve the currently authenticated user's username."

        try:
            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated"}), 401
            
            username = UserServices.get_username_service(user_id)

            return jsonify({"username": username}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def refresh_access_token_controller() -> tuple[Response, int]:
        "Generate a new access token using a valid refresh token."

        try: 
            # Get user ID from the refresh token
            identity = get_jwt_identity()  

            new_access_token = create_access_token(identity=identity)

            expires_at = (datetime.now(timezone.utc) + timedelta(seconds=current_app.config["COOKIE_MAX_AGE"])).timestamp() * 1000

            resp = make_response({"accessTokenExpiresAt": expires_at})

            set_access_cookies(resp, new_access_token, max_age=current_app.config["COOKIE_MAX_AGE"])

            return resp, 200
        
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        