from infrastructure.exception.not_found import NotFound


class PostDoesNotExist(NotFound):
    """
    If post doesn't found by specific criteria, this exception is risen.
    """

    def __init__(self):
        super().__init__("Post doesn't exist.")
