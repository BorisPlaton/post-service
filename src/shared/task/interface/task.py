from abc import ABC
from abc import abstractmethod

from shared.task.interface.dto import ITaskDTO


class ITask(ABC):

    @classmethod
    @abstractmethod
    async def execute(
        cls,
        task_dto: ITaskDTO,
    ) -> None:
        raise NotImplementedError()
