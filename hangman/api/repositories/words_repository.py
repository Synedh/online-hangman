import logging
import random
from pathlib import Path

import requests

logger = logging.getLogger('uvicorn.error')
default_path = Path(__file__).parent.parent / 'words.txt'

class WordsRepo:
    _api_url: str
    _text_path: Path

    def __init__(
            self,
            api_url: str = 'http://localhost:8001',
            text_path: Path = default_path,
        ):
        self._api_url = api_url
        self._text_path = text_path

    def _random_word_fallback(self, size: int | None = None) -> str:
        with open(self._text_path, 'r') as words_file:
            words = words_file.read().splitlines()
        if size:
            words = list(filter(lambda word: len(word) == size, words))
        return random.choice(words)

    def get_random_word(self, size: int | None = None) -> str:
        try:
            response = requests.post(
                f'{self._api_url}/word',
                json={'size': size}
            )
            return response.json()
        except requests.exceptions.RequestException:
            logger.warn('Unreachable word API, falling back to local words file.')
            return self._random_word_fallback(size=size)
