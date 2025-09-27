import math
from typing import Optional
import pygame
from config import core
from hardware.i2c import I2C_BUTTON_RELEASE_EVENT
from states.base import TextAlign, TextPosition
from utils.draw_text import wrap_text


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
        wrap_text_width: Optional[int] = None,
        text_align: TextAlign = "left",
        pulse_text: bool = False,
        button_id: Optional[int] = None,
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
        self.wrap_text_width = wrap_text_width
        self.text_align = text_align
        self.button_id = button_id

        self.pulse_text = pulse_text
        self.pulse_time = 0.0
        self.pulse_speed = 2.5
        self.pulse_min_alpha = 50
        self.pulse_max_alpha = 255
        self.current_alpha = 255

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
        if self.wrap_text_width:
            lines = wrap_text(self.text, self.font, self.wrap_text_width)
            line_surfaces = [self.font.render(line, True, self.text_color) for line in lines]
            width = max(s.get_width() for s in line_surfaces)
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
                s.set_alpha(self.current_alpha)
                self.text_surface.blit(s, (x, y))
                y += s.get_height()
            text_rect = self.text_surface.get_rect()
        else:
            self.text_surface = self.font.render(self.text, True, self.text_color)
            self.text_surface.set_alpha(self.current_alpha)
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
        
    def update_pulse(self, dt: float) -> None:
        if self.pulse_text:
            self.pulse_time += dt * self.pulse_speed
            pulse = (math.sin(self.pulse_time) + 1) / 2  # Range [0, 1]
            alpha = int(self.pulse_min_alpha + pulse * (self.pulse_max_alpha - self.pulse_min_alpha))
            self.current_alpha = alpha
        else:
            self.current_alpha = 255
        self._update_text_rect()

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

        if not hasattr(self, "_last_tick"):
            self._last_tick = pygame.time.get_ticks()
        now = pygame.time.get_ticks()
        dt = (now - self._last_tick) / 1000.0
        self._last_tick = now

        if self.pulse_text:
            self.pulse_time += dt * self.pulse_speed
            pulse = (math.sin(self.pulse_time) + 1) / 2
            alpha = int(self.pulse_min_alpha + pulse * (self.pulse_max_alpha - self.pulse_min_alpha))
            self.current_alpha = alpha
        else:
            self.current_alpha = 255

        self._update_text_rect()

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and event.button == 1:
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.clicked and self.hovered and event.button == 1:
                self.clicked = False
                return True
        elif self.button_id and event.type == I2C_BUTTON_RELEASE_EVENT and hasattr(event, 'button_id'):
            if event.button_id == self.button_id:
                self.clicked = False
                return True
        return False
