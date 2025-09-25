from .repository import UserRepository

from app.features.common.dataclasses import User

from werkzeug.security import generate_password_hash

import uuid

class UserServices:

    @staticmethod
    def user_login_service(email: str, password: str):

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
    def user_signup_service(user_signup_details):
        password_hash = generate_password_hash(user_signup_details['password'])

        user_id = uuid.uuid4()

        UserRepository.user_signup(user_id, user_signup_details['username'], user_signup_details['email'], password_hash)

    def get_username_service(user_id):
        
        username_dict = UserRepository.get_username(user_id)

        return username_dict['username']
