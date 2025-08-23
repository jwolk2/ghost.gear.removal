from typing import Any
import pygame
from config import core, game as cfg
from states.base import (
    BaseState,
    ButtonColor,
    ButtonLocation,
    Choice,
    StateName,
    TextPosition,
)
from ui.button import Button
from ui.sprite import ImageSprite
from ui.text import TextBox

LOCATION_ALIGNMENT: dict[ButtonLocation, TextPosition] = {
    ButtonLocation.TOP: "top-outside",
    ButtonLocation.LEFT: "left-outside",
    ButtonLocation.RIGHT: "right-outside",
}


class GameScreen(BaseState):
    def __init__(
        self, choices: list[Choice], question: str, sprites: list[ImageSprite]
    ) -> None:
        super().__init__()

        if len(choices) < 1:
            raise ValueError("At least one choice is required for the game screen.")
        elif len(choices) > 3:
            raise ValueError(
                "A maximum of three choices is allowed for the game screen."
            )

        self.selection: str | None = None

        button_font = pygame.font.Font(core.HEADING_FONT, cfg.BUTTON_TEXT_FONT_SIZE)

        self.buttons: dict[ButtonLocation, Button] = {}
        for choice in choices:
            if choice.location in self.buttons:
                raise ValueError(
                    f"Multiple choices cannot be assigned to the same location: {choice.location}."
                )
            if choice.color == ButtonColor.RED:
                self.buttons[choice.location] = Button(
                    x=cfg.TOP_BUTTON_X,
                    y=cfg.TOP_BUTTON_Y,
                    text=choice.text,
                    text_color=cfg.BUTTON_TEXT_COLOR,
                    sprite=pygame.image.load(core.RED_BUTTON).convert_alpha(),
                    sprite_hover=pygame.image.load(
                        core.RED_BUTTON_HOVER
                    ).convert_alpha(),
                    text_position=LOCATION_ALIGNMENT[choice.location],
                    font=button_font
                )
            elif choice.color == ButtonColor.GREEN:
                self.buttons[choice.location] = Button(
                    x=cfg.RIGHT_BUTTON_X,
                    y=cfg.RIGHT_BUTTON_Y,
                    text=choice.text,
                    text_color=cfg.BUTTON_TEXT_COLOR,
                    sprite=pygame.image.load(core.GREEN_BUTTON).convert_alpha(),
                    sprite_hover=pygame.image.load(
                        core.GREEN_BUTTON_HOVER
                    ).convert_alpha(),
                    text_position=LOCATION_ALIGNMENT[choice.location],
                    font=button_font
                )
            elif choice.color == ButtonColor.BLUE:
                self.buttons[choice.location] = Button(
                    x=cfg.LEFT_BUTTON_X,
                    y=cfg.LEFT_BUTTON_Y,
                    text=choice.text,
                    text_color=cfg.BUTTON_TEXT_COLOR,
                    sprite=pygame.image.load(core.BLUE_BUTTON).convert_alpha(),
                    sprite_hover=pygame.image.load(
                        core.BLUE_BUTTON_HOVER
                    ).convert_alpha(),
                    text_position=LOCATION_ALIGNMENT[choice.location],
                    font=button_font
                )
            else:
                raise ValueError(
                    f"Unsupported button color option: {choice.color}. The supported colors are: {list(ButtonColor)}."
                )

        self.question_text = TextBox(
            x=cfg.QUESTION_TEXT_X,
            y=cfg.QUESTION_TEXT_Y,
            text=question,
            font_size=cfg.QUESTION_TEXT_FONT_SIZE,
            font=pygame.font.Font(core.HEADING_FONT, cfg.QUESTION_TEXT_FONT_SIZE),
        )

        self.sprites = sprites

    def handle_event(self, event: Any) -> None:
        for button in self.buttons.values():
            if button.handle_event(event):
                self.next_state = StateName.GAME
                self.selection = button.text
                break

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(cfg.GAME_BG_COLOR)
        self.question_text.draw(screen)
        for sprite in self.sprites:
            sprite.draw(screen)
        for button in self.buttons.values():
            button.draw(screen)

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons.values():
            button.update(mouse_pos)
