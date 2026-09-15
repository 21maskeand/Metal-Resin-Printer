from dataclasses import dataclass
from enum import Enum
from typing import Generic , TypeVar

T = TypeVar("T")

class State(Enum):
    SUCCESS = "success"
    ERROR = "error"

@dataclass
class Result(Generic[T]):
    value: T
    message: str = ""
    state: State = State.SUCCESS

    def is_good():
        return self.state is State.SUCCESS