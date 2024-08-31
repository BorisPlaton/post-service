from infrastructure.exception.forbidden import Forbidden


class InvalidPasswordProvided(Forbidden):
    """
    If during log in user provided invalid password, this exception is risen.
    """

    def __init__(self):
        super().__init__("Invalid password provided.")
