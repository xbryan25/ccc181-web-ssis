from flask import Blueprint
from .controllers import UserController

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/login", methods=["POST"])
def user_login():
    return UserController.user_login_controller()

@user_bp.route("/signup", methods=["POST"])
def user_signup():
    return UserController.user_signup_controller()
