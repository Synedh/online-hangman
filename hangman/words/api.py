from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from words.controller import select_word_use_case


api = FastAPI()

class WordBody(BaseModel):
    size: int | None = None


@api.post('/word')
def select_random_word(
        body: WordBody,
) -> str:
    try:
        return select_word_use_case(size=body.size)
    except IndexError:
        raise HTTPException(status_code=400, detail='Invalid word size')
