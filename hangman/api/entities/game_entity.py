from enum import Enum
from uuid import uuid4


def str_uuid() -> str:
    return str(uuid4())


class GameStatus(str, Enum):
    IN_PROGRESS = 'in_progress'
    WON = 'won'
    LOST = 'lost'


class GameIsAlreadyOverError(Exception):
    ...


class Game:
    def __init__(
            self,
            max_errors: int,
            word_to_guess: str,
            id: str | None = None,
            errors: int = 0,
            selected_letters: list[str] | None = None,
    ):
        self._id = id or str_uuid()
        self._max_errors = max_errors
        self._word_to_guess = word_to_guess
        self._errors = errors
        self._selected_letters = selected_letters or []

    @property
    def selected_letters(self) -> list[str]:
        return self._selected_letters

    @property
    def word_to_guess(self) -> str | None:
        return self._word_to_guess

    @property
    def errors(self) -> int:
        return self._errors

    @property
    def id(self) -> str:
        return self._id

    @property
    def max_errors(self) -> int:
        return self._max_errors

    @property
    def word_so_far(self) -> str:
        return ''.join([l if l in self.selected_letters else '_' for l in self.word_to_guess])

    @property
    def errors_left(self) -> int:
        return self.max_errors - self.errors

    @property
    def game_status(self) -> GameStatus:
        if self.max_errors == self.errors:
            return GameStatus.LOST
        elif self.word_so_far == self.word_to_guess:
            return GameStatus.WON
        else:
            return GameStatus.IN_PROGRESS

    def add_selected_letter(self, letter: str) -> None:
        if self.game_status != GameStatus.IN_PROGRESS:
            raise GameIsAlreadyOverError()
        self.selected_letters.append(letter)
        if letter not in self.word_to_guess:
            self._errors += 1
