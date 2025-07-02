from .repositories.game_repository import GamesRepo
from .repositories.words_repository import WordsRepo


class Dependencies:
    games_repo = GamesRepo()
    words_repo = WordsRepo()
