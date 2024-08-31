#!/usr/bin/env python3
from punq import Container
from typer import Context
from typer import Typer

from application.cli.controllers.web import app as web_app
from application.cli.controllers.background import app as background_app
from domain.module import DomainModule
from infrastructure.module import InfrastructureModule
from infrastructure.module_setup.config import ModulesConfig


def create_app() -> Typer:
    """
    The CLI utility for the delivery service application.

    @return:
        Returns a `Typer` instance with all set of CLI commands.
    """
    app = Typer(
        help="The CLI utility for the post service application.",
        no_args_is_help=True,
    )

    app.add_typer(web_app)
    app.add_typer(background_app)

    modules_config = ModulesConfig(
        container=Container(),
        modules=(
            InfrastructureModule(),
            DomainModule(),
        ),
    )
    modules_config.setup()

    @app.callback()
    def set_registry(context: Context) -> None:
        context.obj = modules_config.container

    return app


if __name__ == '__main__':
    create_app()()
