from functools import cached_property

from domain.post.model import PostComment
from domain.post.repository.comment.interface import IPostCommentRepository


class PostCommentRepository(IPostCommentRepository):
    """
    The repository for interaction with post comment model.
    """

    @cached_property
    def entity_class(self) -> type[PostComment]:
        return PostComment
