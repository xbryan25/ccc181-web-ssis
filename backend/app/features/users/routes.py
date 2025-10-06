from flask import Blueprint
from .controllers import UserController

from flask_jwt_extended import jwt_required
user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/login", methods=["POST"])
def user_login():
    """
    Authenticate a user and start a new session.

    This endpoint expects a JSON body containing 'email' and 'password'.
    If authentication is successful, the server sets HTTP-only cookies for the
    access and refresh tokens and returns a success message with session details.

    Request body:

        email: The email address of the user.
        
        password: The password of the user.

    Response JSON:

        username: The username of the authenticated.

        messageTitle: A short success message.

        message: A friendly message for the user.

        accessTokenExpiresAt: Timestamp (in milliseconds) for when the access token expires.

    Possible errors:

        401 if the credentials are invalid.

        500 if an unexpected error occurs during processing.

    Additional notes:

        HTTP-only cookies for access and refresh tokens are also set.
    """
    
    return UserController.user_login_controller()

@user_bp.route("/logout", methods=["POST"])
def user_logout():
    """
    Log out a user and clear their session.

    This endpoint removes authentication cookies to log out the user. It clears both the access and refresh tokens from the client browser.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        messageTitle: A short success message.

        message: A confirmation that the session has been cleared.

    Possible errors:

        500 if an unexpected error occurs during processing.

    Additional notes:

        Both access and refresh cookies are cleared using unset_jwt_cookies().
    """
    
    return UserController.user_logout_controller()

@user_bp.route("/signup", methods=["POST"])
def user_signup():
    """
    Register a new user account.

    This endpoint expects a JSON body containing the registration details of the user. It creates a new user record in the system and returns a success message upon completion.

    Request body:

        username: The desired username for the new account.

        email: The email address of the user.

        password: The password for the new account.

    Response JSON:

        messageTitle: A short success message.

        message: A confirmation that the account has been successfully created.

    Possible errors:

        500 if an unexpected error occurs during processing.
    """

    return UserController.user_signup_controller()

@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """
    Retrieve the currently authenticated user's information.

    This endpoint requires a valid access token (HTTP-only cookie) to identify the user.
    It returns the username associated with the authenticated session.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        username: The username of the currently authenticated user.

    Possible errors:

        401 if the user is not authenticated or the token is missing/invalid.

        500 if an unexpected error occurs during processing.
    """

    return UserController.get_current_user_controller()

@user_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_access_token():
    """
    Generate a new access token using a valid refresh token.

    This endpoint requires a valid refresh token (HTTP-only cookie).
    It issues a new access token and updates the access token cookie without requiring the user to log in again.

    Request body:

        None. This endpoint does not require any input data.

    Response JSON:

        accessTokenExpiresAt: Timestamp (in milliseconds) indicating when the new access token will expire.

    Possible errors:

        401 if the refresh token is missing or invalid.

        500 if an unexpected error occurs during processing.
    """

    return UserController.refresh_access_token_controller()
