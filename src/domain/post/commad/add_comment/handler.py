from domain.post.commad.add_comment.command import AddPostCommentCommand
from domain.post.commad.validate_text.command import ValidateTextCommand
from domain.post.exception.post_doesnt_exist import PostDoesNotExist
from domain.post.model import PostComment
from domain.post.repository.comment.interface import IPostCommentRepository
from domain.post.repository.post.interface import IPostRepository
from shared.message_bus.command_bus.handler.handler import ICommandHandler
from shared.message_bus.command_bus.interface.bus import ICommandBus


class AddPostCommentCommandHandler(ICommandHandler[int, AddPostCommentCommand]):
    """
    Adds a new comment to the specific post.
    """

    def __init__(
        self,
        comment_repository: IPostCommentRepository,
        post_repository: IPostRepository,
        command_bus: ICommandBus,
    ):
        """
        @param comment_repository:
            The repository for comments.
        @param post_repository:
            The repository for posts.
        @param command_bus:
            The command bus for invoking subcommands.
        """
        self._comment_repository = comment_repository
        self._post_repository = post_repository
        self._command_bus = command_bus

    async def __call__(
        self,
        message: AddPostCommentCommand,
    ) -> int:
        """
        Adds a new comment to the specific post and sends event that the comment
        has been created.

        @param message:
            Contains all information about the new comment.
        @raise PostDoesNotExist:
            If the post to which the comment was added does not exist, raises
            an exception.
        @return:
            The new comment's id.
        """
        if not await self._post_repository.get(message.post_id):
            raise PostDoesNotExist()

        comment = PostComment(
            post_id=message.post_id,
            content=message.content,
            author_id=message.author_id,
            blocked=not self._command_bus.handle(
                message=ValidateTextCommand(
                    text=message.content,
                )
            ),
        )
        await self._comment_repository.create(comment)

        return comment.id
