from shared.exception.forbidden import Forbidden


class LoginAlreadyExist(Forbidden):
    """
    If during registration user provided already existed login, this exception
    is risen.
    """

    def __init__(self):
        super().__init__("User with provided login already exists.")
