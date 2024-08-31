from domain.auto_reply.command.configure.command import ConfigureCommentAutoReplyCommand
from domain.auto_reply.repository.configuration.interface import ICommentAutoReplyConfigurationRepository
from infrastructure.message_bus.command_bus.handler.interface import ICommandHandler


class ConfigureCommentAutoReplyCommandHandler(ICommandHandler[ConfigureCommentAutoReplyCommand, None]):
    """
    Configures a comment auto response for the specific user.
    """

    def __init__(
        self,
        comment_auto_reply_configuration_repository: ICommentAutoReplyConfigurationRepository,
    ):
        self._comment_auto_reply_configuration_repository = comment_auto_reply_configuration_repository

    async def __call__(
        self,
        message: ConfigureCommentAutoReplyCommand,
    ) -> None:
        configuration = await self._comment_auto_reply_configuration_repository.get_by_user_id(
            user_id=message.user_id,
        )
        configuration.enabled = message.enabled
        configuration.auto_reply_delay = message.auto_reply_delay

        await self._comment_auto_reply_configuration_repository.update(
            entity=configuration,
        )

