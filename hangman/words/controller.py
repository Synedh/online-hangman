import random
from pathlib import Path

default_path = Path(__file__).parent / 'words.txt'

def select_word_use_case(
        size: int | None = None
    ) -> str:
    with open(default_path, 'r') as words_file:
        words = words_file.read().splitlines()
    if size:
        words = list(filter(lambda word: len(word) == size, words))
    return random.choice(words)
