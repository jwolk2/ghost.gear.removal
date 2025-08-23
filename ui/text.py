from typing import Optional

import pygame
from config import core
from utils.draw_text import wrap_text

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
            tuple[int, int, int] | tuple[int, int, int, int] | None
        ) = None,
        text_color: (
            tuple[int, int, int] | tuple[int, int, int, int]
        ) = core.DEFAULT_TEXT_COLOR,
        text_margin: int = 10,
        font_size: int = core.DEFAULT_TEXT_FONT_SIZE,
        wrap_text_width: Optional[int] = None,
        text_align: str = "left",
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
        self.text_margin = text_margin
        self.font_size = font_size
        self.wrap_text_width = wrap_text_width
        self.text_align = text_align

        self.text_surface = None
        self.text_rect = None
        self._update_text_rect()

    def _update_text_rect(self) -> None:
        # Only wrap if wrap_text_width is set
        if self.wrap_text_width:
            wrap_width = self.wrap_text_width
            lines = wrap_text(self.text, self.font, wrap_width)
            line_surfaces = [self.font.render(line, True, self.text_color) for line in lines]
            width = wrap_width
            height = sum(s.get_height() for s in line_surfaces)
            self.text_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            y = 0
            for s in line_surfaces:
                if self.text_align == "center":
                    x = (width - s.get_width()) // 2
                elif self.text_align == "right":
                    x = width - s.get_width()
                else:  # "left" or fallback
                    x = 0
                self.text_surface.blit(s, (x, y))
                y += s.get_height()
            self.text_rect = self.text_surface.get_rect(topleft=(self.x, self.y))
        else:
            self.text_surface = self.font.render(self.text, True, self.text_color)
            self.text_rect = self.text_surface.get_rect(topleft=(self.x, self.y))

    def draw(self, surface: pygame.Surface) -> None:
        if self.bg_color is not None:
            pygame.draw.rect(surface, self.bg_color, self.rect)
        surface.blit(self.text_surface, self.text_rect)