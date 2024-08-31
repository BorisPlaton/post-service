from punq import Container
from typer import Context
from typer import Typer

from infrastructure.message_bus.command_bus.bus.interface import ICommandBus
from infrastructure.message_bus.command_bus.command import ICommand


app = Typer(
    name='background',
    no_args_is_help=True,
    help='Background processing of application commands.'
)


@app.command()
async def commands(
    context: Context,
    queue_name: str,
) -> None:
    # TODO: Listen queue to get commands from it
    # TODO: Transport command from json to python type
    command: ICommand = ICommand()

    container: Container = context.obj
    await container.resolve(ICommandBus).handle(
        message=command,
    )
