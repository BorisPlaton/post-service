from infrastructure.exception.not_found import NotFound


class CommentDoesNotExist(NotFound):

    def __init__(self):
        super().__init__("Post comment doesn't exist.")