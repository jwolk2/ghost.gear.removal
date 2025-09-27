from typing import Any
import pygame
from config import core, game as cfg
from hardware.i2c import set_led
from states.audio_player import AudioPlayer
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

channel = 0

class GameScreen(BaseState):
    def __init__(
        self, choices: list[Choice], question: str, sprites: list[ImageSprite], sound: str,
    ) -> None:
        global channel
        super().__init__()

        if len(choices) < 1:
            raise ValueError("At least one choice is required for the game screen.")
        elif len(choices) > 3:
            raise ValueError(
                "A maximum of three choices is allowed for the game screen."
            )

        self.selection: str | None = None

        button_font = pygame.font.Font(core.HEADING_FONT, cfg.BUTTON_TEXT_FONT_SIZE)

        self.enabled_leds = []
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
                    font=button_font,
                    wrap_text_width=cfg.BUTTON_TEXT_WRAP_WIDTH,
                    text_align=cfg.BUTTON_TEXT_ALIGN,
                    button_id=core.RED_BUTTON_ID
                )
                self.enabled_leds.append(core.RED_BUTTON_LED_ID)
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
                    font=button_font,
                    wrap_text_width=cfg.BUTTON_TEXT_WRAP_WIDTH,
                    text_align=cfg.BUTTON_TEXT_ALIGN,
                    button_id=core.GREEN_BUTTON_ID
                )
                self.enabled_leds.append(core.GREEN_BUTTON_LED_ID)
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
                    font=button_font,
                    wrap_text_width=cfg.BUTTON_TEXT_WRAP_WIDTH,
                    text_align=cfg.BUTTON_TEXT_ALIGN,
                    button_id=core.BLUE_BUTTON_ID
                )
                self.enabled_leds.append(core.BLUE_BUTTON_LED_ID)
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
            wrap_text_width=cfg.QUESTION_TEXT_WRAP_WIDTH,
            text_align=cfg.QUESTION_TEXT_ALIGN,
        )

        self.sprites = sprites

        channel += 1
        self.sound_player = AudioPlayer(narration_sound=sound, channel=channel, repeat=core.REPEAT_NARRATION, repeat_interval=core.REPEAT_NARRATION_DELAY)
        self.sound_started = False
        self.other_leds = [led for led in self.leds or [] if led not in self.enabled_leds]

    def handle_event(self, event: Any) -> bool:
        for button in self.buttons.values():
            if button.handle_event(event):
                self.next_state = StateName.GAME
                self.selection = button.text
                self.sound_player.reset()
                return True
        return False

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(cfg.GAME_BG_COLOR)
        self.question_text.draw(screen)
        for sprite in self.sprites:
            sprite.draw(screen)
        for button in self.buttons.values():
            button.draw(screen)

    def update(self) -> None:
        if not self.sound_started:
            self.sound_player.play()
            self.sound_started = True
        self.sound_player.update()
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons.values():
            button.update(mouse_pos)
        for led in self.enabled_leds:
            set_led(led, True)
        for led in self.other_leds:
            set_led(led, False)

    def reset(self) -> None:
        self.next_state = None
        self.selection = None
        self.sound_player.reset()
        self.sound_started = False
