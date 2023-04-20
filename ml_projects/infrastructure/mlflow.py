import mlflow

from ml_projects.config import settings


def init_mlflow():
    mlflow.set_tracking_uri(settings.Settings.MLFLOW_TRACKING_URI)
