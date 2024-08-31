from dataclasses import dataclass

from punq import Container


@dataclass(kw_only=True, slots=True)
class CLIExecutionContext:
    container: Container
