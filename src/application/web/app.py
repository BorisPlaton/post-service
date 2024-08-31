from typing import Awaitable
from typing import Callable

from fastapi import FastAPI
from fastapi import Request
from punq import Container

from domain.module import DomainModule
from infrastructure.settings.app import ApplicationSettings
from infrastructure.exception.base import BaseAppException
from application.web.exception.factory import exception_factory
from infrastructure.module import InfrastructureModule
from infrastructure.module_setup.config import ModulesConfig
from domain.user.controller.rest.api import tag as user_tag
from domain.user.controller.rest.api import router as user_router
from domain.post.controller.rest.api import tag as post_tag
from domain.post.controller.rest.api import router as post_router
from domain.auto_reply.controller.rest.api import tag as auto_response_tag
from domain.auto_reply.controller.rest.api import router as auto_response_router


def create_app() -> FastAPI:
    """
    Creates an application and configures DI-container.

    @return:
        The initialized FastAPI application.
    """
    modules_config = ModulesConfig(
        container=Container(),
        modules=(
            InfrastructureModule(),
            DomainModule(),
        ),
    )
    modules_config.setup()

    app_settings: ApplicationSettings = modules_config.container.resolve(ApplicationSettings)

    app = FastAPI(
        debug=app_settings.DEBUG,
        description=app_settings.DESCRIPTION,
        version=app_settings.VERSION,
        openapi_tags=[
            {
                "name": user_tag,
                "description": "Operations with users. This section has endpoints for login/register operation.",
            },
            {
                "name": post_tag,
                "description": "Operations with posts. Has operation to create post/comments and"
                               " to retrieve aggregated statistics for them.",
            },
            {
                "name": auto_response_tag,
                "description": "Operations for the comment auto reply functionality.",
            },
        ],
    )
    app.include_router(user_router)
    app.include_router(post_router)
    app.include_router(auto_response_router)

    @app.middleware('http')
    async def set_registry[T](
        request: Request,
        call_next: Callable[[Request], Awaitable[T]],
    ) -> T:
        request.state.registry = modules_config.container
        return await call_next(request)

    @app.exception_handler(BaseAppException)
    def base_app_exception_handler(
        request: Request,
        exc: BaseAppException,
    ) -> None:
        raise exception_factory(exc=exc)

    return app
