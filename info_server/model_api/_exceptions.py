class ModelAPIException(Exception):
    """Base class for exceptions in ModelAPI."""
    pass


class ModelGroupNotFoundError(ModelAPIException):
    """Raised when an API group is not found."""
    pass

class APIKeyNotSetError(ModelAPIException):
    """Raised when an API key is not set."""
    pass