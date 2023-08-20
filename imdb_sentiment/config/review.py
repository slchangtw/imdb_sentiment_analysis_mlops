from pydantic import BaseSettings


class Review(BaseSettings):
    text: str
