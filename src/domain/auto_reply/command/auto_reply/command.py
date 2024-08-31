from dataclasses import dataclass
from dataclasses import field

from infrastructure.message_bus.command_bus.command import ICommand
from infrastructure.message_bus.command_bus.config.mixin.abstract import AbstractConfigurableCommand
from infrastructure.message_bus.command_bus.config.options.background import BackgroundExecutionOption
from infrastructure.message_bus.command_bus.config.options.base import ICommandOptions
from infrastructure.message_bus.command_bus.config.options.transactional import TransactionalOption


@dataclass(kw_only=True, slots=True)
class AutoReplyCommentCommand(
    ICommand,
    AbstractConfigurableCommand,
):
    """
    Auto reply for the new created comment.
    """
    post_id: int
    comment_id: int
    comment_author_id: int
    post_author_id: int

    command_config: dict[type[ICommandOptions], ICommandOptions] = field(
        # TODO: Refactor it to not use lambda syntax
        default_factory=lambda: {
            BackgroundExecutionOption: BackgroundExecutionOption(
                is_background=True
            ),
            TransactionalOption: TransactionalOption(
                is_transactional=True,
            ),
        }

    )
