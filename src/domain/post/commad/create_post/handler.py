from domain.post.commad.create_post.command import CreatePostCommand
from domain.post.commad.validate_text.command import ValidateTextCommand
from domain.post.model import Post
from domain.post.repository.post.interface import IPostRepository
from shared.message_bus.command_bus.handler.handler import ICommandHandler
from shared.message_bus.command_bus.interface.bus import ICommandBus


class CreatePostCommandHandler(ICommandHandler[int, CreatePostCommand]):
    """
    Creates a new post.
    """

    def __init__(
        self,
        post_repository: IPostRepository,
        command_bus: ICommandBus,
    ):
        """
        @param post_repository:
            The repository for posts.
        """
        self._post_repository = post_repository
        self._command_bus = command_bus

    async def __call__(
        self,
        message: CreatePostCommand,
    ) -> int:
        """
        Creates a new post and sends event that post has been created.

        @param message:
            Contains all information about the post.
        @return:
            The new post record id.
        """
        post = Post.create(
            content=message.content,
            title=message.title,
            author_id=message.author_id,
            blocked=not self._command_bus.handle(
                message=ValidateTextCommand(
                    text=f"{message.title} {message.content}",
                )
            ),
        )
        await self._post_repository.create(post)

        return post.id
