from flask import request, jsonify
from dataclasses import asdict

from flask_jwt_extended import create_access_token

import traceback

from .services import UserServices


class UserController:
 

    @staticmethod
    def user_login_controller():

        user_details = request.json

        try:
            user = UserServices.user_login_service(user_details.get('email'), user_details.get('password'))
            
            if not user:
                return jsonify({"error": "Invalid credentials."}), 401
            
            access_token = create_access_token(identity=user.user_id)

            return jsonify({
                "accessToken": access_token,
                "username": user.username,
            }), 200
        
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500