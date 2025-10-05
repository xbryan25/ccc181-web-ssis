from flask import Blueprint
from .controllers import UserController

from flask_jwt_extended import jwt_required

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/login", methods=["POST"])
def user_login():
    return UserController.user_login_controller()

@user_bp.route("/logout", methods=["POST"])
def user_logout():
    return UserController.user_logout_controller()

@user_bp.route("/signup", methods=["POST"])
def user_signup():
    return UserController.user_signup_controller()

@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    return UserController.get_current_user_controller()
