import time
import pygame

from config import core

pygame.mixer.init()

class AudioPlayer:
    def __init__(self, narration_sound: str, channel: int = 0, repeat: bool = True, repeat_interval: int = 30) -> None:
        self.narration_sound = narration_sound
        self.channel = pygame.mixer.Channel(channel)
        self.sound = pygame.mixer.Sound(self.narration_sound)
        self.repeat = repeat
        self.repeat_interval = repeat_interval  # in seconds
        self._last_end_time = None

        self.channel.set_volume(core.SOUND_PLAYER_VOLUME)

    def play(self) -> None:
        if not self.channel.get_busy():
            self.channel.play(self.sound)
            self._last_end_time = None

    def stop(self) -> None:
        if self.channel.get_busy():
            self.channel.stop()
        self._last_end_time = None

    def is_playing(self) -> bool:
        return self.channel.get_busy()
    
    def set_sound(self) -> None:
        self.stop()
        self.sound = pygame.mixer.Sound(self.narration_sound)

    def update(self) -> None:
        if not self.is_playing():
            if self._last_end_time is None:
                self._last_end_time = time.time()
            elif self.repeat and (time.time() - self._last_end_time >= self.repeat_interval):
                self.play()

    def reset(self) -> None:
        self.stop()
        self._last_end_time = None