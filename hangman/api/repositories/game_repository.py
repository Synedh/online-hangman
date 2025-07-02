import json
from pathlib import Path

from api.entities.game_entity import Game
from api.models.game_model import GameModel

default_path = Path(__file__).parent.parent / 'games.json'

class GamesRepo:
    _games: dict[str, Game]
    _save_path: Path

    def __init__(self, save_path: Path = default_path):
        self._games = {}
        self._save_path = save_path

    def save(self, game: Game):
        with open(self._save_path, 'r') as save_file:
            games = json.load(save_file)
        games[game.id] = {
            'id': game.id,
            'max_errors': game.max_errors,
            'word_to_guess': game.word_to_guess,
            'errors': game.errors,
            'selected_letters': game.selected_letters,
        }
        with open(self._save_path, 'w') as save_file:
            json.dump(games, save_file)

    def get(self, game_id: str) -> Game:
        with open(self._save_path, 'r') as save_file:
            games = json.load(save_file)
        if game_id not in games:
            raise ValueError(f'Game with id {game_id} not found')

        game_dict = games[game_id]
        return Game(
            id=game_dict['id'],
            max_errors=game_dict['max_errors'],
            word_to_guess=game_dict['word_to_guess'],
            errors=game_dict['errors'],
            selected_letters=game_dict['selected_letters'],
        )
