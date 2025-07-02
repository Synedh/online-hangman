from api.entities.game_entity import Game, GameStatus

from pydantic import BaseModel

class GameModel(BaseModel):
    id: str
    max_errors: int
    word_to_guess: str | None
    errors: int
    selected_letters: list[str]
    word_so_far: str
    errors_left: int
    game_status: GameStatus

    @staticmethod
    def from_game(game: Game) -> 'GameModel':
        word_to_guess = None if game.game_status == GameStatus.IN_PROGRESS else game.word_to_guess
        return GameModel(
            id=game.id,
            max_errors=game.max_errors,
            word_to_guess=word_to_guess,
            errors=game.errors,
            selected_letters=game.selected_letters,
            word_so_far=game.word_so_far,
            errors_left=game.errors_left,
            game_status=game.game_status,
        )
