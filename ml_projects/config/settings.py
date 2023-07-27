from pydantic import BaseSettings


class Settings(BaseSettings):
    MLFLOW_TRACKING_URI: str = "sqlite:///mlflow.db"


settings = Settings(
    _env_file_encoding="utf-8",
)
