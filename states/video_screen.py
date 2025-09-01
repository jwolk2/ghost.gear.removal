import pygame
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
        if self.video.active is False:
            self.video.close()
            self.next_state = StateName.START
            self.done = True

    def draw(self, screen: Surface) -> None:
        self.video.draw(screen, (0, 0))

    def reset(self) -> None:
        self.next_state = None
        self.done = False
        self.video.stop()