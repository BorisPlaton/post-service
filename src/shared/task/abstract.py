import asyncio

from punq import Container

from shared.module_setup.config import ModulesConfig
from shared.task.interface.dto import ITaskDTO
from shared.task.interface.task import ITask


class AbstractTask[U: ITaskDTO](ITask):

    @classmethod
    def execute(
        cls,
        dto: U,
    ) -> None:
        asyncio.run(cls(dto=dto)())

    def __init__(
        self,
        dto: U,
    ):
        self.dto = dto
        self.container = Container()
        ModulesConfig(
            container=self.container,
            modules=dto.modules,
        ).setup()

    async def __call__(self) -> None:
        raise NotImplementedError()
