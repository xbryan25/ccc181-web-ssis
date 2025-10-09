class ValidationError(Exception):
    """Raised when user input validation fails."""
    pass

class EntityNotFoundError(Exception):
    """Raised when an entity is not found."""
    pass