import pygame
from config import core as cfg

pygame.init()
screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Ghost Gear Removal")


import sys

from states.base import StateName
from states.manager import GameScreenManager
from states.start_screen import StartScreen
from states.game_screen import GameScreen

clock = pygame.time.Clock()

# State management
current_state = StartScreen()
game_screen_manager = GameScreenManager()
game_started = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        current_state.handle_event(event)

    current_state.update()
    current_state.draw(screen)

    if current_state.next_state:
        if current_state.next_state == StateName.GAME:
            if not game_started:
                current_state = game_screen_manager.get_current_screen()
                game_started = True
            else:
                next_state = game_screen_manager.get_next_screen()

                # If the next state is the same as the current state, it means we are at the end of the game screens.
                # In that case, we reset the next_state to prevent any logical errors.
                if next_state != current_state:
                    current_state = next_state
                else:
                    # TODO: Start the video playback
                    current_state.next_state = None
        else:
            current_state = StartScreen()
    pygame.display.flip()
    clock.tick(cfg.FPS)
