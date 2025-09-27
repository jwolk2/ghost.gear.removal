import pygame
from hardware.i2c import set_led
from states.base import BaseState, StateName
from pygame.surface import Surface
from pyvidplayer2 import Video


class VideoScreen(BaseState):
    def __init__(self, video_path: str) -> None:
        super().__init__()
        self.video = Video(video_path, use_pygame_audio=True)
        self.done = False

    def handle_event(self, event) -> bool:
        return False

    def update(self) -> None:
        self.video.update()
        for led in self.leds or []:
            set_led(led, False)
        if self.video.active is False:
            self.video.close()
            self.next_state = StateName.START
            self.done = True

    def draw(self, screen: Surface) -> None:
        screen_width, screen_height = screen.get_size()
        frame_surf = self.video.frame_surf

        if frame_surf is None:
            # No frame to draw yet, fill screen with black
            screen.fill((0, 0, 0))
            return

        video_width, video_height = frame_surf.get_size()

        # Calculate scale to fit inside screen (no stretch)
        scale = min(screen_width / video_width, screen_height / video_height)
        new_width = int(video_width * scale)
        new_height = int(video_height * scale)

        # Center the video
        x = (screen_width - new_width) // 2
        y = (screen_height - new_height) // 2

        # Scale and blit
        scaled_frame = pygame.transform.smoothscale(frame_surf, (new_width, new_height))
        screen.blit(scaled_frame, (x, y))

    def reset(self) -> None:
        self.next_state = None
        self.done = False
        self.video.stop()
