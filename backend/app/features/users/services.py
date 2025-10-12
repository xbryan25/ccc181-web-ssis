from .repository import UserRepository

from app.features.common.dataclasses import User

from werkzeug.security import generate_password_hash

import uuid

from app.exceptions.custom_exceptions import ValidationError

class UserServices:

    @staticmethod
    def user_login_service(email: str, password: str) -> User:
        """
        Authenticate a user with email and password.
        
        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: A User dataclass instance if credentials are correct, otherwise None.
        """

        user = UserRepository.get_user_by_email(email)

        if not user:
            return None

        user["user_id"] = str(user["user_id"])

        # Convert dict to dataclass
        user_dataclass = User(**user)

        # Verify password
        if user_dataclass.check_password(password):
            return user_dataclass
        
        return None
    
    @staticmethod
    def user_signup_service(user_signup_details) -> None:
        """
        Register a new user using the provided signup details.

        Args:
            user_signup_details (dict): A dictionary containing the user's signup information.
                Expected keys include:
                    - "email" (str): The email address of the user.
                    - "username" (str): The desired username.
                    - "password" (str): The password of the user.
        """

        password_hash = generate_password_hash(user_signup_details['password'].strip())

        user_id = uuid.uuid4()

        UserRepository.user_signup(user_id, user_signup_details['username'], user_signup_details['email'], password_hash)

    def get_username_service(user_id) -> str:
        """
        Get the username of a user using the user_id.

        Args:
            user_id (str): user_id of the user.

        Returns:
            str: The username of the user if found, otherwise None.
        """
        
        username_dict = UserRepository.get_username(user_id)

        return username_dict['username']
    
    @staticmethod
    def validate_signup_details(email, username):
        """
        Validates email and username. If either email or username has already been taken, then ValidationError will be raised.

        Args:
            email (str): The email to be checked.
            username (str): The username to be checked
        """

        if UserServices.check_email_if_it_exists_service(email):
            raise ValidationError(f"The email '{email}' has already been taken.")
        if UserServices.check_username_if_it_exists_service(username):
            raise ValidationError(f"The username '{username}' has already been taken.")
    
    def check_email_if_it_exists_service(email) -> bool:
        """
        Checks if email has already been taken.

        Args:
            email (str): The email to be checked.

        Returns:
            bool: Returns True if the email has already been taken, otherwise False.
        """

        result_dict = UserRepository.check_email_if_it_exists(email)

        return result_dict['exists']
    
    def check_username_if_it_exists_service(username) -> bool:
        """
        Checks if username has already been taken.

        Args:
            username (str): The username to be checked.

        Returns:
            bool: Returns True if the username has already been taken, otherwise False.
        """

        result_dict = UserRepository.check_username_if_it_exists(username)

        return result_dict['exists']
    