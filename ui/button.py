from typing import Optional
import pygame
from config import core
from states.base import TextPosition


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        width: int = core.DEFAULT_BUTTON_WIDTH,
        height: int = core.DEFAULT_BUTTON_HEIGHT,
        text: str = core.DEFAULT_BUTTON_TEXT,
        font: Optional[pygame.font.Font] = None,
        bg_color: tuple[int, int, int] = core.DEFAULT_BUTTON_BG_COLOR,
        text_color: tuple[int, int, int] = core.DEFAULT_BUTTON_TEXT_COLOR,
        hover_color: tuple[int, int, int] = core.DEFAULT_BUTTON_HOVER_COLOR,
        border_radius: int = core.DEFAULT_BUTTON_BORDER_RADIUS,
        sprite: Optional[pygame.Surface] = None,
        sprite_hover: Optional[pygame.Surface] = None,
        text_position: TextPosition = "center",
        text_margin: int = 10,
    ) -> None:
        if font is None:
            font = pygame.font.Font(core.DEFAULT_FONT, core.DEFAULT_BUTTON_FONT_SIZE)

        if sprite is None and (width is None or height is None):
            raise ValueError(
                "Either width and height for a rect or a sprite must be provided."
            )

        self.x = x
        self.y = y
        self.sprite = sprite
        self.sprite_hover = sprite_hover

        if sprite is None:
            self.rect = pygame.Rect(x, y, width, height)
            self.bg_color = bg_color
            self.hover_color = hover_color
        else:
            sprite_width, sprite_height = sprite.get_size()
            self.rect = pygame.Rect(x, y, sprite_width, sprite_height)
            self.bg_color = (0, 0, 0)
            self.hover_color = (0, 0, 0)

        self.text = text
        self.font = font
        self.text_color = text_color
        self.border_radius = border_radius
        self.clicked = False
        self.hovered = False
        self.text_position = text_position
        self.text_margin = text_margin

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
        if self.sprite:
            if self.hovered and self.sprite_hover:
                surface.blit(self.sprite_hover, self.rect.topleft)
            else:
                surface.blit(self.sprite, self.rect.topleft)
        else:
            color = self.hover_color if self.hovered else self.bg_color
            pygame.draw.rect(
                surface, color, self.rect, border_radius=self.border_radius
            )

        surface.blit(self.text_surface, self.text_rect)

    def update(self, mouse_pos: tuple[int, int]) -> None:
        if self.sprite:
            rel_x = mouse_pos[0] - self.rect.x
            rel_y = mouse_pos[1] - self.rect.y
            sprite_width, sprite_height = self.sprite.get_size()
            if 0 <= rel_x < sprite_width and 0 <= rel_y < sprite_height:
                pixel = self.sprite.get_at((rel_x, rel_y))
                self.hovered = pixel.a > 0
            else:
                self.hovered = False
        else:
            self.hovered = self.rect.collidepoint(mouse_pos)
        self._update_text_rect()

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and event.button == 1:
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.clicked and self.hovered and event.button == 1:
                self.clicked = False
                return True
        return False
