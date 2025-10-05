from flask import request, jsonify, make_response, current_app

from flask_jwt_extended import create_access_token, get_jwt_identity, set_access_cookies, unset_jwt_cookies, get_jwt

import traceback

from .services import UserServices


class UserController:
 
    @staticmethod
    def user_login_controller():

        user_login_details = request.json

        try:
            user = UserServices.user_login_service(user_login_details.get('email'), user_login_details.get('password'))
            
            if not user:
                return jsonify({"error": "Invalid credentials."}), 401
            
            access_token = create_access_token(identity=user.user_id)

            resp = make_response({
                "username": user.username,
                "messageTitle": "Login successful.",
                "message": "Enjoy your session!"
            })
            
            set_access_cookies(resp, access_token, max_age=current_app.config["COOKIE_MAX_AGE"])

            return resp, 200
        
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def user_logout_controller():

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
    def user_signup_controller():

        user_signup_details = request.json

        try:
            UserServices.user_signup_service(user_signup_details)
            
            return jsonify({"messageTitle": "Signup successful.", "message": "Your account is ready. Enjoy using Sequence!"}), 201
        
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def get_current_user_controller():

        try:
            user_id = get_jwt_identity()

            if not user_id:
                return jsonify({"message": "Not authenticated"}), 401
            
            username = UserServices.get_username_service(user_id)

            return jsonify({"username": username}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
        