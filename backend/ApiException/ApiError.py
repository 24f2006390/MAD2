class APIError(Exception):
    """Base Exception for all API-related errors."""

    def __init__(self, message_dict, status_code=400):
        super().__init__()
        self.message_dict = message_dict
        self.status_code = status_code


class NotFoundError(APIError):
    """Raised when a requested resource is not found in the system."""

    pass


class AuthenticationError(APIError):
    """Raised when user credentials fail validation."""

    pass


class ValidationError(APIError):
    """Raised when input data fails business logic validation."""

    pass
