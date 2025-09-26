import os

# Cookie max age is in minutes
def get_cookie_max_age(default: str = 5) -> int:
    value = os.getenv("COOKIE_MAX_AGE", default)

    try:
        return int(value)
    except ValueError:
        print(f"WARNING: COOKIE_MAX_AGE='{value}' is not a valid integer. Using default={default}")
        return int(default)
