import re
from app.exceptions.custom_exceptions import ValidationError

EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
USERNAME_REGEX = r"^[A-Za-z0-9_.-]{3,20}$"

def validate_email_format(email: str) -> None:
    """Validates inputted email according to EMAIL_REGEX."""

    email = email.strip()

    if not email:
        raise ValidationError("Email cannot be blank.")
    if not re.match(EMAIL_REGEX, email):
        raise ValidationError(f"The email '{email}' is not in the proper format.")

def validate_username_format(username: str) -> None:
    """Validates inputted username according to USERNAME_REGEX."""

    username = username.strip()

    if not username:
        raise ValidationError("Username cannot be blank.")
    
    if len(username) < 3:
        raise ValidationError("Username must be at least 3 characters long.")
    if len(username) > 20:
        raise ValidationError("Username must not exceed 20 characters.")

    if not re.match(USERNAME_REGEX, username):
        raise ValidationError(f"The username '{username}' is not in the proper format.")

def validate_password(password: str) -> None:
    """Validates inputted password."""

    password = password.strip()

    if not password:
        raise ValidationError("Password cannot be blank.")

    if " " in password:
        raise ValidationError("Password cannot contain spaces.")

    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if len(password) > 64:
        raise ValidationError("Password must not exceed 64 characters.")

    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one number.")
    if not re.search(r"[@$!%*?&]", password):
        raise ValidationError("Password must contain at least one special character (@$!%*?&).")
