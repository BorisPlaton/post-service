from domain.post.commad.create_post.command import CreatePostCommand
from domain.post.commad.validate_text.command import ValidateTextCommand
from domain.post.model import Post
from domain.post.repository.post.interface import IPostRepository
from infrastructure.message_bus.command_bus.handler.interface import ICommandHandler
from infrastructure.message_bus.command_bus.bus.interface import ICommandBus


class CreatePostCommandHandler(ICommandHandler[CreatePostCommand, int]):
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
        Creates a new post and moderates it via AI.

        @param message:
            Contains all information about the post.
        @return:
            The new post record id.
        """
        post = Post.create(
            content=message.content,
            title=message.title,
            author_id=message.author_id,
            blocked=not await self._command_bus.handle(
                message=ValidateTextCommand(
                    text=f"{message.title} {message.content}",
                )
            ),
        )
        await self._post_repository.create(post)

        return post.id
