from typing import Optional

import pygame
from config import core
from states.base import TextPosition


class TextBox:
    def __init__(
        self,
        x: int,
        y: int,
        width: int = core.DEFAULT_TEXT_WIDTH,
        height: int = core.DEFAULT_TEXT_HEIGHT,
        text: str = core.DEFAULT_TEXT,
        font: Optional[pygame.font.Font] = None,
        bg_color: (
            tuple[int, int, int] | tuple[int, int, int, int]
        ) = core.DEFAULT_TEXT_BG_COLOR,
        text_color: (
            tuple[int, int, int] | tuple[int, int, int, int]
        ) = core.DEFAULT_TEXT_COLOR,
        text_position: TextPosition = "center",
        text_margin: int = 10,
        font_size: int = core.DEFAULT_TEXT_FONT_SIZE,
    ) -> None:
        if font is None:
            font = pygame.font.Font(core.DEFAULT_FONT, font_size)

        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color

        self.text = text
        self.font = font
        self.text_color = text_color
        self.clicked = False
        self.hovered = False
        self.text_position = text_position
        self.text_margin = text_margin
        self.font_size = font_size

        self.text_surface = self.font.render(self.text, True, self.text_color)
        self._update_text_rect()

    def _update_text_rect(self) -> None:
        self.text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = self.text_surface.get_rect()

        # Anchor text based on position relative to button
        if self.text_position == "center":
            self.text_rect = text_rect.copy()
            self.text_rect.center = self.rect.center

        elif self.text_position == "left":
            self.text_rect = text_rect.copy()
            self.text_rect.midleft = self.rect.midleft
        elif self.text_position == "right":
            self.text_rect = text_rect.copy()
            self.text_rect.midright = self.rect.midright
        elif self.text_position == "top":
            self.text_rect = text_rect.copy()
            self.text_rect.midtop = self.rect.midtop
        elif self.text_position == "bottom":
            self.text_rect = text_rect.copy()
            self.text_rect.midbottom = self.rect.midbottom

        # Outside the button
        elif self.text_position == "left-outside":
            self.text_rect = text_rect.copy()
            self.text_rect.centery = self.rect.centery
            self.text_rect.right = self.rect.left - self.text_margin
        elif self.text_position == "right-outside":
            self.text_rect = text_rect.copy()
            self.text_rect.centery = self.rect.centery
            self.text_rect.left = self.rect.right + self.text_margin
        elif self.text_position == "top-outside":
            self.text_rect = text_rect.copy()
            self.text_rect.centerx = self.rect.centerx
            self.text_rect.bottom = self.rect.top - self.text_margin
        elif self.text_position == "bottom-outside":
            self.text_rect = text_rect.copy()
            self.text_rect.centerx = self.rect.centerx
            self.text_rect.top = self.rect.bottom + self.text_margin
        else:
            raise ValueError(f"Unknown text_position: {self.text_position}")

    def draw(self, surface: pygame.Surface) -> None:
        if self.bg_color:
            if len(self.bg_color) == 4:  # RGBA
                bg_surface = pygame.Surface(
                    (self.rect.width, self.rect.height), pygame.SRCALPHA
                )
                bg_surface.fill(self.bg_color)
                surface.blit(bg_surface, self.rect)
            else:  # RGB
                pygame.draw.rect(surface, self.bg_color, self.rect)

        # Render text with possible RGBA color
        if len(self.text_color) == 4:  # RGBA text
            self.text_surface = self.font.render(self.text, True, self.text_color[:3])
            self.text_surface.set_alpha(self.text_color[3])
        else:
            self.text_surface = self.font.render(self.text, True, self.text_color)

        surface.blit(self.text_surface, self.text_rect)

    def update(self, mouse_pos: tuple[int, int]) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> bool:
        return True
