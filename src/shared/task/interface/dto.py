from abc import ABC
from dataclasses import dataclass
from typing import Iterable

from shared.module_setup.module import IModule


@dataclass(kw_only=True, slots=True, frozen=True)
class ITaskDTO(ABC):
    modules: Iterable[IModule]
