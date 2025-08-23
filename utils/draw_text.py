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

def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + (' ' if current_line else '') + word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines
