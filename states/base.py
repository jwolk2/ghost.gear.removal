from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Literal, Optional


class StateName(Enum):
    START = auto()
    GAME = auto()


class ButtonColor(Enum):
    GREEN = auto()
    BLUE = auto()
    RED = auto()


class ButtonLocation(Enum):
    TOP = auto()
    LEFT = auto()
    RIGHT = auto()


class BaseState(ABC):
    def __init__(self) -> None:
        self.next_state: Optional[StateName] = None

    @abstractmethod
    def handle_event(self, event: Any) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self, screen: Any) -> None:
        pass


class Choice:
    def __init__(self, text: str, color: ButtonColor, location: ButtonLocation) -> None:
        self.text = text
        self.color = color
        self.location = location


TextPosition = Literal[
    "center",
    "left",
    "right",
    "top",
    "bottom",
    "left-outside",
    "right-outside",
    "top-outside",
    "bottom-outside",
]

TextAlign = Literal["left", "center", "right"]
