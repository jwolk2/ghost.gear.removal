import time
import pygame
from config import core as cfg
from hardware.i2c import poll_buttons, i2c_reset

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(
    (cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT), pygame.FULLSCREEN
)
pygame.display.set_caption("Ghost Gear Removal")


import sys

from states.base import StateName
from states.manager import GameScreenManager
from states.start_screen import StartScreen
from states.game_screen import GameScreen
from states.video_screen import VideoScreen

clock = pygame.time.Clock()

# State management
start_screen = StartScreen()
current_state = start_screen
game_screen_manager = GameScreenManager()
game_started = False

last_interaction_time = time.time()
last_mouse_move_time = time.time()

try:
    while True:
        current_time = time.time()
        poll_buttons()  # Poll I2C buttons each frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i2c_reset()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(True)
                last_mouse_move_time = current_time

            state_flag = current_state.handle_event(event)
            if state_flag:
                last_interaction_time = current_time
        
        if current_time - last_mouse_move_time > cfg.MOUSE_HIDE_DELAY:
            pygame.mouse.set_visible(False)

        # Check for inactivity
        if current_time - last_interaction_time > cfg.INACTIVITY_TIMEOUT:
            # Timeout: reset to StartScreen
            current_state.reset()
            game_screen_manager.reset()
            start_screen.reset()
            current_state = start_screen
            game_started = False
            last_interaction_time = current_time

        current_state.update()
        current_state.draw(screen)

        if current_state.next_state:
            if current_state.next_state == StateName.GAME:
                if not game_started:
                    # Show the first game screen
                    current_state = game_screen_manager.get_current_screen()
                    game_started = True
                else:
                    # Only advance if a selection was made
                    if hasattr(current_state, "selection") and current_state.selection:
                        next_state = game_screen_manager.get_next_screen()
                        if next_state != current_state:
                            current_state = next_state
                        else:
                            # End of game screens: resolve video
                            video_path = game_screen_manager.resolve_video()
                            current_state = VideoScreen(video_path)
            else:
                current_state.reset()
                game_screen_manager.reset()
                start_screen.reset()
                current_state = start_screen
                game_started = False
                last_interaction_time = time.time()
        pygame.display.flip()
        clock.tick(cfg.FPS)
except KeyboardInterrupt:
    i2c_reset()
    pygame.quit()
    sys.exit()
