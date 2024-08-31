from infrastructure.exception.not_found import NotFound


class UserWithProvidedLoginDoesntExist(NotFound):
    """
    If no user found with provided login, this exception is risen.
    """

    def __init__(self):
        super().__init__("User with provided login doesn't exist.")
