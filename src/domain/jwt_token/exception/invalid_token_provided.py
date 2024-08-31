from infrastructure.exception.forbidden import Forbidden


class InvalidTokenProvided(Forbidden):
    """
    If the provided JWT is of invalid format, this exception is raised.
    """

    def __init__(self):
        super().__init__("Invalid token provided.")
