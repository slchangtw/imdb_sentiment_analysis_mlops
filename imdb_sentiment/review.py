from pydantic_settings import BaseSettings


class Review(BaseSettings):
    text: str
