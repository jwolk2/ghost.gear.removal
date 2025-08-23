import pygame
from pygame.surface import Surface
from pygame.event import Event
from config import start as cfg
from config import core
from states.base import BaseState, StateName
from ui.button import Button
from ui.sprite import ImageSprite
from ui.text import TextBox
from utils.draw_text import draw_text


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
            sprite=pygame.image.load(core.GREEN_BUTTON).convert_alpha(),
            sprite_hover=pygame.image.load(core.GREEN_BUTTON_HOVER).convert_alpha(),
        )

        self.title_text = TextBox(
            x=cfg.TITLE_TEXT_X,
            y=cfg.TITLE_TEXT_Y,
            text=cfg.TITLE_TEXT,
            font=pygame.font.Font(core.TITLE_FONT, cfg.TITLE_TEXT_FONT_SIZE),
        )

    def handle_event(self, event: Event) -> None:
        if self.button.handle_event(event):
            self.next_state = StateName.GAME

    def draw(self, screen: Surface) -> None:
        screen.fill(cfg.START_BG_COLOR)
        self.title_text.draw(screen)
        self.button.draw(screen)

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.button.update(mouse_pos)
