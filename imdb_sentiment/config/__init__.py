import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

from .params import params

project_folder = Path(__file__).parent

load_dotenv(project_folder / ".env")


class Settings(BaseSettings):
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    EXPERIMENT_NAME: str = "imdb_sentiment_analysis"
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")

    # Hyperparameter tuning space
    PARAMS = params


settings = Settings(
    _env_file_encoding="utf-8",
)
