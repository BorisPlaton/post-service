from shared.exception.not_found import NotFound


class CommentAuthorDoesNotExist(NotFound):

    def __init__(self):
        super().__init__("Comment's author doesnt exist.")
