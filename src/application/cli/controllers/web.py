from typing import Annotated

import uvicorn
from typer import Option
from typer import Typer


app = Typer(
    name='web',
    no_args_is_help=True,
    help='Set of commands for the web part of application.'
)


@app.command()
def up(
    port: Annotated[int, Option(help='The port number of the app.')] = 8000,
    workers: Annotated[int, Option(help='Workers quantity of the app.')] = 4,
    debug: Annotated[bool, Option(help='Launches the app in the debug mode.')] = False,
) -> None:
    """
    Starts the web-application.
    """
    uvicorn.run(
        app='application.web.app:create_app',
        host='0.0.0.0',
        port=port,
        workers=workers,
        reload=debug,
        factory=True,
    )
