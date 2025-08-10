import pygame
from config import core as cfg

def draw_text(
    screen: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
    center: bool = False,
    x: int = 0,
    y: int = 0
) -> None:
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (cfg.SCREEN_WIDTH // 2, cfg.SCREEN_HEIGHT // 2)
    else:
        rect.topleft = (x, y)
    screen.blit(rendered, rect)
