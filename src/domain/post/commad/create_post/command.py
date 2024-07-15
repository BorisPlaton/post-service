from dataclasses import dataclass

from shared.message_bus.command_bus.interface.command import ICommand


@dataclass(kw_only=True, slots=True)
class CreatePostCommand(ICommand):
    """
    Command to create a new post.
    """
    content: str
    title: str
    author_id: int
