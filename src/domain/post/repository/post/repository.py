from functools import cached_property

from domain.post.model import Post
from domain.post.repository.post.interface import IPostRepository


class PostRepository(IPostRepository):
    """
    The repository for interacting with post model.
    """

    @cached_property
    def entity_class(self) -> type[Post]:
        return Post
