from domain.post.commad.add_comment.command import AddPostCommentCommand
from domain.post.commad.validate_text.command import ValidateTextCommand
from domain.post.event.new_comment_created import NewCommentCreatedEvent
from domain.post.exception.post_doesnt_exist import PostDoesNotExist
from domain.post.model import PostComment
from domain.post.repository.comment.interface import IPostCommentRepository
from domain.post.repository.post.interface import IPostRepository
from infrastructure.message_bus.command_bus.handler.interface import ICommandHandler
from infrastructure.message_bus.command_bus.bus.interface import ICommandBus
from infrastructure.message_bus.event_bus.bus.interface import IEventBus


class AddPostCommentCommandHandler(ICommandHandler[AddPostCommentCommand, int]):
    """
    Adds a new comment to the specific post.
    """

    def __init__(
        self,
        comment_repository: IPostCommentRepository,
        post_repository: IPostRepository,
        command_bus: ICommandBus,
        event_bus: IEventBus,
    ):
        """
        @param comment_repository:
            The repository for comments.
        @param post_repository:
            The repository for posts.
        @param command_bus:
            The command bus for invoking subcommands.
        @param event_bus:
            The event bus for pushing new event.
        """
        self._comment_repository = comment_repository
        self._post_repository = post_repository
        self._command_bus = command_bus
        self._event_bus = event_bus

    async def __call__(
        self,
        message: AddPostCommentCommand,
    ) -> int:
        """
        Adds a new comment to the specific post and moderates it via AI.

        @param message:
            Contains all information about the new comment.
        @raise PostDoesNotExist:
            If the post to which the comment was added does not exist, raises
            an exception.
        @return:
            The new comment's id.
        """
        post = await self._post_repository.get(message.post_id)

        if not post:
            raise PostDoesNotExist()

        blocked = not await self._command_bus.handle(
            message=ValidateTextCommand(
                text=message.content,
            )
        )
        comment = PostComment(
            post_id=message.post_id,
            content=message.content,
            author_id=message.author_id,
            blocked=blocked,
        )
        await self._comment_repository.create(comment)

        await self._event_bus.handle(
            message=NewCommentCreatedEvent(
                comment_id=comment.id,
                comment_author_id=message.author_id,
                post_author_id=post.author_id,
                post_id=message.post_id,
                blocked=blocked,
            )
        )

        return comment.id
