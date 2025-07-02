from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .controllers.game_controller import (guess_letter_use_case,
                                          init_game_use_case)
from .entities.game_entity import GameIsAlreadyOverError
from .models.game_model import GameModel

api = FastAPI()

class CreateGameBody(BaseModel):
    max_errors: int = 5
    word_size: int | None = None


@api.post('/games')
def create_game(
        create_game_body: CreateGameBody,
) -> GameModel:
    game = init_game_use_case(
        max_errors=create_game_body.max_errors,
        word_size=create_game_body.word_size,
    )
    return GameModel.from_game(game)


class Letter(BaseModel):
    letter: str


@api.post('/games/{game_id}/selected_letters')
def add_selected_letter(
        game_id: str,
        letter: Letter,
) -> GameModel:
    try:
        game = guess_letter_use_case(game_id=game_id, letter=letter.letter)
        return GameModel.from_game(game)
    except GameIsAlreadyOverError:
        raise HTTPException(status_code=400, detail='Game is already over')
