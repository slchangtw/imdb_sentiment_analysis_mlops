from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    EXPERIMENT_NAME: str = "imdb_sentiment_analysis"
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"


settings = Settings(
    _env_file_encoding="utf-8",
)
