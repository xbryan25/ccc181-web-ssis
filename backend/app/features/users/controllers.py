from flask import request, jsonify, make_response
from dataclasses import asdict

from flask_jwt_extended import create_access_token

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
                "message": "Login successful."
            })
            
            # HttpOnly cookie, cannot be read by JS
            resp.set_cookie(
                "accessToken",
                access_token,
                httponly=True,
                secure=True, 
                samesite="Strict"
            )

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
        