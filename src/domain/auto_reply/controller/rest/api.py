from typing import Annotated

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import status
from punq import Container

from domain.auto_reply.command.configure.command import ConfigureCommentAutoReplyCommand
from domain.auto_reply.controller.rest.contracts.input.configure import \
    ConfigureCommentAutoReplyConfigurationInputContract
from domain.auto_reply.controller.rest.contracts.output.configuration import CommentAutoReplyConfigurationOutputContract
from domain.auto_reply.repository.configuration.interface import ICommentAutoResponseConfigurationRepository
from domain.user.controller.rest.dependency.user import get_user
from domain.user.model import User
from shared.fastapi_.dependency.registry import get_registry
from shared.message_bus.command_bus.bus.interface import ICommandBus


router = APIRouter(
    prefix='/auto-response',
    tags=[tag := 'Comment Auto Response'],
)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
)
async def get_auto_reply_config(
    user: Annotated[User, Depends(get_user)],
    registry: Annotated[Container, Depends(get_registry)],
) -> CommentAutoReplyConfigurationOutputContract:
    """
    Returns a user's auto reply configuration.
    """
    return await registry.resolve(ICommentAutoResponseConfigurationRepository).get_by_user_id(
        user_id=user.id,
    )


@router.post(
    '/configure/',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def configure_auto_reply(
    user: Annotated[User, Depends(get_user)],
    configuration: Annotated[
        ConfigureCommentAutoReplyConfigurationInputContract,
        Body(description=ConfigureCommentAutoReplyConfigurationInputContract.__doc__),
    ],
    registry: Annotated[Container, Depends(get_registry)],
) -> None:
    """
    Configures the auto response for the specific user.
    """
    return await registry.resolve(ICommandBus).handle(
        message=ConfigureCommentAutoReplyCommand(
            user_id=user.id,
            enabled=configuration.enabled,
            auto_reply_delay=configuration.auto_reply_delay,
        ),
    )
