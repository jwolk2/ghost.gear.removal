from collections import deque
from typing import List
from data_structures.doubly_linked_list import DoublyLinkedList, Node
from states.game_screen import GameScreen
from states.base import ButtonLocation, Choice, ButtonColor
from ui.sprite import ImageSprite
from config import game as cfg


class GameScreenRegistry:
    """
    Registry for managing game screens with choices.
    Stores instances of GameScreen in a doubly linked list.
    Allows for easy addition and retrieval of game screens, while maintaining order.
    """

    def __init__(self):
        self._screens: DoublyLinkedList[GameScreen] = DoublyLinkedList()

    def register(
        self, choices: List[Choice], question: str, sprites: list[ImageSprite]
    ) -> None:
        self._screens.append(GameScreen(choices, question, sprites))

    def first(self) -> Node[GameScreen]:
        if self._screens.head is None:
            raise ValueError("No game screens registered.")
        return self._screens.head


registry = GameScreenRegistry()
# Registering screens in the order they should be displayed
registry.register(
    choices=[
        Choice(text="Option A", color=ButtonColor.GREEN, location=ButtonLocation.RIGHT),
        Choice(text="Option B", color=ButtonColor.BLUE, location=ButtonLocation.LEFT),
        Choice(text="Option C", color=ButtonColor.RED, location=ButtonLocation.TOP),
    ],
    question="What would you like to do first?",
    sprites=[
        ImageSprite(
            x=cfg.FISH_X,
            y=cfg.FISH_Y,
            image=cfg.FISH_IMAGE,
            width=cfg.FISH_WIDTH,
            rotation=cfg.FISH_ROTATION,
        )
    ],
)
registry.register(
    choices=[
        Choice(text="Option A", color=ButtonColor.GREEN, location=ButtonLocation.RIGHT),
        Choice(text="Option B", color=ButtonColor.BLUE, location=ButtonLocation.LEFT),
    ],
    question="What would you like to do next?",
    sprites=[],
)
