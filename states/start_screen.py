import pygame
from pygame.surface import Surface
from pygame.event import Event
from config import start as cfg
from config import core
from hardware.i2c import set_led
from states.audio_player import AudioPlayer
from states.base import BaseState, StateName
from ui.button import Button
from ui.sprite import ImageSprite
from ui.text import TextBox


class StartScreen(BaseState):
    def __init__(self) -> None:
        super().__init__()
        self.font: pygame.font.Font = pygame.font.Font(
            core.DEFAULT_FONT, cfg.START_FONT_SIZE
        )

        self.button = Button(
            x=cfg.START_BUTTON_X,
            y=cfg.START_BUTTON_Y,
            text=cfg.START_BUTTON_TEXT,
            font=self.font,
            text_color=cfg.START_BUTTON_TEXT_COLOR,
            sprite=pygame.image.load(core.RED_BUTTON).convert_alpha(),
            sprite_hover=pygame.image.load(core.RED_BUTTON_HOVER).convert_alpha(),
            text_position="top-outside",
            text_margin=cfg.START_BUTTON_TEXT_MARGIN,
            pulse_text=True,
            button_id=core.RED_BUTTON_ID
        )

        self.title_text = TextBox(
            x=cfg.TITLE_TEXT_X,
            y=cfg.TITLE_TEXT_Y,
            text=cfg.TITLE_TEXT,
            font=pygame.font.Font(core.TITLE_FONT, cfg.TITLE_TEXT_FONT_SIZE),
            text_color=cfg.START_TEXT_COLOR,
            wrap_text_width=cfg.TITLE_TEXT_WRAP_WIDTH,
            text_align=cfg.TITLE_TEXT_ALIGN,
        )

        self.background = ImageSprite(
            x=cfg.BACKGROUND_OFFSET_X,
            y=0,
            image=cfg.BACKGROUND_IMAGE,
            width=core.SCREEN_WIDTH,
            height=core.SCREEN_HEIGHT,
        )

        self.sound = core.START_SCREEN_NARRATION
        self.sound_player = AudioPlayer(narration_sound=self.sound, channel=0, repeat=core.REPEAT_NARRATION, repeat_interval=core.REPEAT_NARRATION_DELAY)
        self.sound_started = False
        self.enabled_leds = [core.RED_BUTTON_LED_ID]
        self.other_leds = [led for led in self.leds or [] if led not in self.enabled_leds]

    def handle_event(self, event: Event) -> bool:
        if self.button.handle_event(event):
            self.next_state = StateName.GAME
            self.sound_player.reset()
            return True
        return False

    def draw(self, screen: Surface) -> None:
        screen.fill(cfg.START_BG_COLOR)
        self.background.draw(screen)
        self.title_text.draw(screen)
        self.button.draw(screen)

    def update(self) -> None:
        if not self.sound_started:
            self.sound_player.play()
            self.sound_started = True
        self.sound_player.update()
        mouse_pos = pygame.mouse.get_pos()
        self.button.update(mouse_pos)
        for led in self.enabled_leds:
            set_led(led, True)
        for led in self.other_leds:
            set_led(led, False)

    def reset(self) -> None:
        self.next_state = None
        self.sound_player.reset()
        self.sound_started = False
