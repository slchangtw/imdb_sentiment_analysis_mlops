import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    EXPERIMENT_NAME: str = "imdb_sentiment_analysis"


settings = Settings(
    _env_file_encoding="utf-8",
)
