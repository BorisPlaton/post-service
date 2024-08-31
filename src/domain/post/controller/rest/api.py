from typing import Annotated

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Path
from fastapi import status
from punq import Container

from domain.post.controller.rest.contracts.output.blocked_comments_statistics import \
    PostCommentBlockStatisticsOutputContract
from domain.post.controller.rest.contracts.output.blocked_posts_statistics import PostBlockStatisticsOutputContract
from domain.post.controller.rest.dependency.statistics_range.dependency import get_statistics_range
from domain.post.controller.rest.dependency.statistics_range.type import StatisticsRangeType
from domain.post.controller.rest.contracts.input.comment import NewPostCommentInput
from domain.post.controller.rest.contracts.input.post import NewPostInput
from domain.post.controller.rest.contracts.output.comment import PostCommentOutput
from domain.post.controller.rest.contracts.output.post import PostOutput
from domain.post.model import PostComment
from domain.post.service.comment.interface import IPostCommentService
from domain.post.service.post.interface import IPostService
from domain.user.controller.rest.dependency.user import get_user
from domain.user.model import User
from application.web.dependency import get_registry
from infrastructure.message_bus.command_bus.bus.interface import ICommandBus


router = APIRouter(
    prefix='/post',
    tags=[tag := 'Post'],
)


@router.get(
    '/{post_id:int}/',
    status_code=status.HTTP_200_OK,
)
async def get_post_by_id(
    post_id: Annotated[int, Path(description="The post's `id`.", ge=1)],
    registry: Annotated[Container, Depends(get_registry)],
) -> PostOutput:
    """
    Returns a specific post by its `id`.
    """
    return await registry.resolve(IPostService).get_post(post_id=post_id)


@router.get(
    '/{post_id:int}/comment/',
    status_code=status.HTTP_200_OK,
)
async def get_post_comments(
    post_id: Annotated[int, Path(description="The post's `id`.", ge=1)],
    registry: Annotated[Container, Depends(get_registry)],
) -> list[PostCommentOutput]:
    """
    Returns all comments for a specific post.
    """
    return await registry.resolve(IPostCommentService).get_post_comments(
        post_id=post_id,
        order_by=(PostComment.created_at,)
    )


@router.get(
    '/comment/blocked/',
    status_code=status.HTTP_200_OK,
)
async def get_blocked_comments_statistics(
    _: Annotated[User, Depends(get_user)],
    registry: Annotated[Container, Depends(get_registry)],
    date_range: Annotated[StatisticsRangeType, Depends(get_statistics_range)],
) -> list[PostCommentBlockStatisticsOutputContract]:
    """
    Returns a statistic about blocked comments for some time range.

    It contains aggregated statistic for all days in the provided range:
    * how many comments were written in this day
    * how many comments were blocked in this day
    """
    return await registry.resolve(IPostCommentService).get_statistics(
        from_=date_range.from_,
        to=date_range.to,
    )


@router.get(
    '/blocked/',
    status_code=status.HTTP_200_OK,
)
async def get_blocked_posts_statistics(
    _: Annotated[User, Depends(get_user)],
    registry: Annotated[Container, Depends(get_registry)],
    date_range: Annotated[StatisticsRangeType, Depends(get_statistics_range)],
) -> list[PostBlockStatisticsOutputContract]:
    """
    Returns a statistic about blocked posts for some time range.

    It contains aggregated statistic for all days in the provided range:
    * how many posts were written in this day
    * how many posts were blocked in this day
    """
    return await registry.resolve(IPostService).get_statistics(
        from_=date_range.from_,
        to=date_range.to,
    )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post_data: Annotated[NewPostInput, Body(description=NewPostInput.__doc__)],
    registry: Annotated[Container, Depends(get_registry)],
    user: Annotated[User, Depends(get_user)],
) -> int:
    """
    Creates a new post and returns its `id`.
    """
    return await registry.resolve(ICommandBus).handle(
        message=post_data.to_command(
            user_id=user.id,
        ),
    )


@router.post(
    '/{post_id:int}/comment/',
    status_code=status.HTTP_201_CREATED,
)
async def add_comment_to_post(
    post_id: Annotated[int, Path(description="The post's `id`.", ge=1)],
    comment_data: Annotated[NewPostCommentInput, Body(description=NewPostCommentInput.__doc__)],
    registry: Annotated[Container, Depends(get_registry)],
    user: Annotated[User, Depends(get_user)],
) -> int:
    """
    Adds a comment to a post and returns comment's `id`.
    """
    return await registry.resolve(ICommandBus).handle(
        message=comment_data.to_command(
            user_id=user.id,
            post_id=post_id,
        ),
    )
