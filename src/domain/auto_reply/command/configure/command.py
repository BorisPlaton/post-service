from dataclasses import dataclass

from shared.message_bus.command_bus.command import ICommand


@dataclass(kw_only=True, slots=True)
class ConfigureCommentAutoReplyCommand(ICommand):
    """
    Command to configure auto response for the new comment.
    """
    user_id: int
    enabled: bool
    auto_reply_delay: int
