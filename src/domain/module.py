from punq import Container

from domain.ai.component.client.client import AIClient
from domain.ai.component.client.interface import IAIClient
from domain.auto_reply.command.auto_reply.command import AutoReplyCommentCommand
from domain.auto_reply.command.auto_reply.handler import AutoReplyCommentCommandHandler
from domain.auto_reply.command.configure.command import ConfigureCommentAutoReplyCommand
from domain.auto_reply.command.configure.handler import ConfigureCommentAutoReplyCommandHandler
from domain.auto_reply.event_handler.delay_response_for_new_comment import AutoReplyForNewComment
from domain.auto_reply.repository.configuration.interface import ICommentAutoReplyConfigurationRepository
from domain.auto_reply.repository.configuration.repository import DelayedCommentResponseConfigurationRepository
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
from domain.post.event.new_comment_created import NewCommentCreatedEvent
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
from infrastructure.settings.ai import AISettings
from infrastructure.settings.app import ApplicationSettings
from infrastructure.database.sqlalchemy.connection.interface import IAsyncSQLAlchemyConnectionManager
from infrastructure.message_bus.command_bus.bus.interface import ICommandBus
from infrastructure.message_bus.event_bus.bus.interface import IEventBus
from infrastructure.module_setup.interface import IModule
from infrastructure.redis_.client.interface import IRedisClient


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
        self._register_event_handlers(
            container=container,
        )

    @staticmethod
    def _configure_dependencies(container: Container) -> None:
        container.register(
            service=IUserRepository,
            instance=UserRepository(
                connection_manager=container.resolve(IAsyncSQLAlchemyConnectionManager),
            ),
        )

        container.register(
            service=IPostRepository,
            instance=PostRepository(
                connection_manager=container.resolve(IAsyncSQLAlchemyConnectionManager),
            ),
        )
        container.register(
            service=IPostCommentRepository,
            instance=PostCommentRepository(
                connection_manager=container.resolve(IAsyncSQLAlchemyConnectionManager),
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

        container.register(
            service=IAIClient,
            instance=AIClient(
                settings=container.resolve(AISettings),
            ),
        )
        container.register(
            service=ICommentAutoReplyConfigurationRepository,
            instance=DelayedCommentResponseConfigurationRepository(
                connection_manager=container.resolve(IAsyncSQLAlchemyConnectionManager),
            ),
        )

    @staticmethod
    def _register_commands(container: Container) -> None:
        command_bus: ICommandBus = container.resolve(ICommandBus)

        command_bus.register(
            message=RegisterUserCommand,
            handler=RegisterUserCommandHandler(
                user_repository=container.resolve(IUserRepository),
                delayed_comment_response_configuration_repository=container.resolve(
                    ICommentAutoReplyConfigurationRepository,
                )
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
                event_bus=container.resolve(IEventBus),
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

        command_bus.register(
            message=ConfigureCommentAutoReplyCommand,
            handler=ConfigureCommentAutoReplyCommandHandler(
                comment_auto_reply_configuration_repository=container.resolve(
                    ICommentAutoReplyConfigurationRepository
                ),
            ),
        )
        command_bus.register(
            message=AutoReplyCommentCommand,
            handler=AutoReplyCommentCommandHandler(
                user_repository=container.resolve(IUserRepository),
                post_repository=container.resolve(IPostRepository),
                post_comment_repository=container.resolve(IPostCommentRepository),
                ai_client=container.resolve(IAIClient),
            ),
        )

    @staticmethod
    def _register_event_handlers(container: Container) -> None:
        event_bus = container.resolve(IEventBus)

        event_bus.register(
            message=NewCommentCreatedEvent,
            handler=AutoReplyForNewComment(
                configuration_repository=container.resolve(ICommentAutoReplyConfigurationRepository),
                ai_client=container.resolve(IAIClient),
                post_comment_repository=container.resolve(IPostCommentRepository),
                post_repository=container.resolve(IPostRepository),
                user_repository=container.resolve(IUserRepository),
                redis_client=container.resolve(IRedisClient),
                command_bus=container.resolve(ICommandBus),
            ),
        )
