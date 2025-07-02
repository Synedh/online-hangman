from api.dependencies import Dependencies
from api.entities.game_entity import Game
from api.repositories.game_repository import GamesRepo
from api.repositories.words_repository import WordsRepo


dependencies = Dependencies()

def init_game_use_case(
        max_errors: int,
        word_size: int | None = None,
        games_repo: GamesRepo = dependencies.games_repo,
        words_repo: WordsRepo = dependencies.words_repo,
) -> Game:
    game = Game(
        max_errors=max_errors,
        word_to_guess=words_repo.get_random_word(size=word_size),
    )
    games_repo.save(game=game)
    return game


def guess_letter_use_case(
        game_id: str,
        letter: str,
        games_repo: GamesRepo = dependencies.games_repo,
) -> Game:
    game = games_repo.get(game_id=game_id)
    game.add_selected_letter(letter=letter)
    games_repo.save(game=game)
    return game
