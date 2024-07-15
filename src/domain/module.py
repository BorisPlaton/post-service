import google.generativeai
from punq import Container

from domain.ai.component.client.client import AIClient
from domain.ai.component.client.interface import IAIClient
from domain.jwt_token.command.issue_jwt.command import IssueJWTCommand
from domain.jwt_token.command.issue_jwt.handler import IssueJWTCommandHandler
from domain.jwt_token.command.validate_jwt.command import ValidateJWTCommand
from domain.jwt_token.command.validate_jwt.handler import ValidateJWTCommandHandler
from domain.post.commad.add_comment.command import AddPostCommentCommand
from domain.post.commad.add_comment.handler import AddPostCommentCommandHandler
from domain.post.commad.create_post.command import CreatePostCommand
from domain.post.commad.create_post.handler import CreatePostCommandHandler
from domain.post.commad.validate_text.command import ValidateTextCommand
from domain.post.commad.validate_text.handler import ValidateTextCommandHandler
from domain.post.repository.comment.interface import IPostCommentRepository
from domain.post.repository.comment.repository import PostCommentRepository
from domain.post.repository.post.interface import IPostRepository
from domain.post.repository.post.repository import PostRepository
from domain.post.service.comment.interface import IPostCommentService
from domain.post.service.comment.service import PostCommentService
from domain.post.service.post.interface import IPostService
from domain.post.service.post.service import PostService
from domain.user.command.login.command import LogInUserCommand
from domain.user.command.login.handler import LogInUserCommandHandler
from domain.user.command.register.command import RegisterUserCommand
from domain.user.command.register.handler import RegisterUserCommandHandler
from domain.user.repository.user.interface import IUserRepository
from domain.user.repository.user.repository import UserRepository
from settings.config.app import ApplicationSettings
from settings.config.gemini import GeminiSettings
from shared.database.sqlalchemy.connection.interface import IAsyncSQLAlchemyConnection
from shared.message_bus.command_bus.interface.bus import ICommandBus
from shared.module_setup.module import IModule


class DomainModule(IModule):

    def configure(
        self,
        container: Container,
    ) -> None:
        self._configure_dependencies(
            container=container,
        )
        self._register_commands(
            container=container,
        )

    @staticmethod
    def _configure_dependencies(container: Container) -> None:
        container.register(
            service=IUserRepository,
            instance=UserRepository(
                async_connection=container.resolve(IAsyncSQLAlchemyConnection),
            ),
        )

        container.register(
            service=IPostRepository,
            instance=PostRepository(
                async_connection=container.resolve(IAsyncSQLAlchemyConnection),
            ),
        )
        container.register(
            service=IPostCommentRepository,
            instance=PostCommentRepository(
                async_connection=container.resolve(IAsyncSQLAlchemyConnection),
            ),
        )
        container.register(
            service=IPostService,
            instance=PostService(
                post_repository=container.resolve(IPostRepository),
            ),
        )
        container.register(
            service=IPostCommentService,
            instance=PostCommentService(
                post_service=container.resolve(IPostRepository),
                post_comment_repository=container.resolve(IPostCommentRepository),
            ),
        )

        google.generativeai.configure(
            api_key=container.resolve(GeminiSettings).API_KEY,
        )
        container.register(
            service=IAIClient,
            instance=AIClient(),
        )

    @staticmethod
    def _register_commands(container: Container) -> None:
        command_bus: ICommandBus = container.resolve(ICommandBus)

        command_bus.register(
            message=RegisterUserCommand,
            handler=RegisterUserCommandHandler(
                user_repository=container.resolve(IUserRepository),
            ),
        )
        command_bus.register(
            message=LogInUserCommand,
            handler=LogInUserCommandHandler(
                user_repository=container.resolve(IUserRepository),
                command_bus=command_bus,
            ),
        )

        command_bus.register(
            message=IssueJWTCommand,
            handler=IssueJWTCommandHandler(
                secret_key=container.resolve(ApplicationSettings).SECRET_KEY,
            ),
        )
        command_bus.register(
            message=ValidateJWTCommand,
            handler=ValidateJWTCommandHandler(
                secret_key=container.resolve(ApplicationSettings).SECRET_KEY,
            ),
        )

        command_bus.register(
            message=AddPostCommentCommand,
            handler=AddPostCommentCommandHandler(
                comment_repository=container.resolve(IPostCommentRepository),
                post_repository=container.resolve(IPostRepository),
                command_bus=command_bus,
            ),
        )
        command_bus.register(
            message=CreatePostCommand,
            handler=CreatePostCommandHandler(
                post_repository=container.resolve(IPostRepository),
                command_bus=command_bus,
            ),
        )
        command_bus.register(
            message=ValidateTextCommand,
            handler=ValidateTextCommandHandler(
                ai_client=container.resolve(IAIClient)
            )
        )
