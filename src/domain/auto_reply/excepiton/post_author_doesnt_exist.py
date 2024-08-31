from infrastructure.exception.not_found import NotFound


class PostAuthorDoesNotExist(NotFound):

    def __init__(self):
        super().__init__("Post's author doesnt exist.")
