import os
from config import choices
from states.game_screen import GameScreen
from states.registry import registry


class GameScreenManager:
    def __init__(self):
        self._current = registry.first()
        self._selections: list[str] = []

    def get_current_screen(self) -> GameScreen:
        return self._current.data

    def get_next_screen(self) -> GameScreen:
        """
        Move to the next game screen in the registry.
        If there is no next screen, return the current screen.

        Returns:
            GameScreen: The next game screen or the current one if at the end.
        """
        next = self._current.next
        self._selections.append(self._current.data.selection)
        if next is not None:
            if not self._current.data.selection:
                raise ValueError(
                    "Current screen selection is None. Ensure a choice is made before proceeding."
                )
            self._current = next
            return next.data
        return self.get_current_screen()

    def get_previous_screen(self) -> GameScreen:
        """
        Move to the previous game screen in the registry.
        If there is no previous screen, return the current screen.

        Returns:
            GameScreen: The previous game screen or the current one if at the start.
        """
        prev = self._current.prev
        if prev is not None:
            self._current = prev
            if not self._current.data.selection:
                raise ValueError(
                    "Previous screen selection is None. Ensure a choice was made before proceeding."
                )
            self._selections.remove(self._current.data.selection)
            return prev.data
        return self.get_current_screen()
    
    def resolve_video(self) -> str:
        """
        Resolve the video file path based on the selections made in the game screens.

        Returns:
            str: The file path of the video to be played.
        """
        if not self._selections:
            raise ValueError("No selections made. Cannot resolve video.")
        
        video_path = choices.video_path(self._selections)
        
        assert os.path.exists(video_path), f"Video file does not exist: {video_path}"
        return video_path
    
    def reset(self) -> None:
        """Reset selections and current screen to the first."""
        self._selections.clear()
        self._current = registry.first()
        registry.reset()
