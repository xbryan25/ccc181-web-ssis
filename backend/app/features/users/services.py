from .repository import UserRepository

from app.features.common.dataclasses import User

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
    
