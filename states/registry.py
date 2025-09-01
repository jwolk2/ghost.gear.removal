from collections import deque
from typing import List
from data_structures.doubly_linked_list import DoublyLinkedList, Node
from states.game_screen import GameScreen
from states.base import ButtonLocation, Choice, ButtonColor
from ui.sprite import ImageSprite
from config import game as cfg
from config import choices
from config import core


class GameScreenRegistry:
    """
    Registry for managing game screens with choices.
    Stores instances of GameScreen in a doubly linked list.
    Allows for easy addition and retrieval of game screens, while maintaining order.
    """

    def __init__(self):
        self._screens: DoublyLinkedList[GameScreen] = DoublyLinkedList()

    def register(
        self, choices: List[Choice], question: str, sprites: list[ImageSprite], sound: str
    ) -> None:
        self._screens.append(GameScreen(choices, question, sprites, sound))

    def first(self) -> Node[GameScreen]:
        if self._screens.head is None:
            raise ValueError("No game screens registered.")
        return self._screens.head
    
    def reset(self) -> None:
        node = self._screens.head
        while node:
            node.data.reset()
            node = node.next


registry = GameScreenRegistry()
# Registering screens in the order they should be displayed
registry.register(
    choices=[
        Choice(text=choices.IN_BETWEEN, color=ButtonColor.GREEN, location=ButtonLocation.RIGHT),
        Choice(text=choices.HOUR_BEFORE, color=ButtonColor.BLUE, location=ButtonLocation.LEFT),
        Choice(text=choices.RIGHT_AT, color=ButtonColor.RED, location=ButtonLocation.TOP),
    ],
    question=choices.FIRST_QUESTION,
    sprites=[
        ImageSprite(
            x=cfg.ROV_X,
            y=cfg.ROV_Y,
            image=cfg.ROV_IMAGE,
            width=cfg.ROV_WIDTH,
            rotation=cfg.ROV_ROTATION,
        ),
        ImageSprite(
            x=cfg.TEXT_BUBBLE_X,
            y=cfg.TEXT_BUBBLE_Y,
            image=cfg.TEXT_BUBBLE_IMAGE,
            width=cfg.TEXT_BUBBLE_WIDTH,
            rotation=cfg.TEXT_BUBBLE_ROTATION,
        ),
    ],
    sound=core.GAME_SCREEN_1_NARRATION,
)
registry.register(
    choices=[
        Choice(text=choices.CUT_NET, color=ButtonColor.GREEN, location=ButtonLocation.RIGHT),
        Choice(text=choices.ATTACH_BUOYS, color=ButtonColor.BLUE, location=ButtonLocation.LEFT),
    ],
    question=choices.SECOND_QUESTION,
    sprites=[
        ImageSprite(
            x=cfg.SHEARS_X,
            y=cfg.SHEARS_Y,
            image=cfg.SHEARS_IMAGE,
            width=cfg.SHEARS_WIDTH,
            rotation=cfg.SHEARS_ROTATION,
        ),
        ImageSprite(
            x=cfg.BUOY_X,
            y=cfg.BUOY_Y,
            image=cfg.BUOY_IMAGE,
            width=cfg.BUOY_WIDTH,
            rotation=cfg.BUOY_ROTATION,
        ),
    ],
    sound=core.GAME_SCREEN_2_NARRATION,
)
