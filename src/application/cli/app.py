#!/usr/bin/env python3

from typer import Typer

from application.cli.controllers.web import app as app_typer


def create_app() -> Typer:
    """
    The CLI utility for the delivery service application.

    @return:
        Returns a `Typer` instance with all set of CLI commands.
    """
    app = Typer(
        help="The CLI utility for the delivery service application.",
        no_args_is_help=True,
    )

    app.add_typer(app_typer)

    return app


if __name__ == '__main__':
    create_app()()
