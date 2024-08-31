from infrastructure.exception.forbidden import Forbidden


class ExpiredTokenProvided(Forbidden):
    """
    Exception when JWT is expired.
    """

    def __init__(self):
        super().__init__("Provided token is expired.")
