from dataclasses import dataclass

from shared.message_bus.command_bus.interface.command import ICommand


@dataclass(kw_only=True, slots=True)
class AddPostCommentCommand(ICommand):
    """
    Command to add a comment to a post.
    """
    content: str
    author_id: int
    post_id: int
