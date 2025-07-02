from enum import Enum

import requests
import typer

app = typer.Typer()

class GameStatus(str, Enum):
    IN_PROGRESS = 'in_progress'
    WON = 'won'
    LOST = 'lost'


def init_game(
        api_url: str,
        max_errors: int,
        word_size: str | None = None,
) -> dict:
    response = requests.post(
        f'{api_url}/games',
        json={'max_errors': max_errors, 'word_size': word_size}
    )
    return response.json()


def guess_letter(
        api_url: str,
        game_id: str,
        letter: str,
) -> dict:
    response = requests.post(
        f'{api_url}/games/{game_id}/selected_letters',
        json={'letter': letter}
    )
    return response.json()


@app.command()
def hangman(
        api_url: str = typer.Option('http://localhost:8000', '--api-url', help='Set the API URL'),
        max_errors: int = typer.Option(5, '-e', help='Set the maximum number of errors allowed'),
        word_size: int | None = typer.Option(None, '-s', help='Set the size of the word to guess'),
):
    print('###################')
    print('Starting new game !')
    print('###################')

    # init game
    game = init_game(api_url=api_url, max_errors=max_errors, word_size=word_size)

    while True:
        print(f'Your word so far is: {game['word_so_far']}')

        letter = input(f'You have {game['errors_left']} errors left. Enter a letter: ')

        if len(letter) == 1 and letter.isalpha():
            game = guess_letter(api_url=api_url, game_id=game['id'], letter=letter)

            if game['game_status'] == GameStatus.WON:
                print('You won \o/')
                print(f'The word was {game['word_to_guess']}')
                break
            elif game['game_status'] == GameStatus.LOST:
                print('You lost :(')
                print(f'The word was {game['word_to_guess']}')
                break
        else:
            print('you didn\'t enter a letter')
