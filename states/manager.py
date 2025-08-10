from states.base import Choice
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
        if next is not None:
            if not self._current.data.selection:
                raise ValueError(
                    "Current screen selection is None. Ensure a choice is made before proceeding."
                )
            self._selections.append(self._current.data.selection)
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
