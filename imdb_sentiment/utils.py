import pickle
from pathlib import Path

import git
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient
from sklearn.pipeline import Pipeline

from imdb_sentiment.config import settings


def get_git_sha() -> str:
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    return sha


def get_best_run_id() -> str:
    client = MlflowClient(tracking_uri=settings.MLFLOW_TRACKING_URI)
    experiment_id = client.get_experiment_by_name(
        settings.EXPERIMENT_NAME
    ).experiment_id

    best_runs = client.search_runs(
        experiment_ids=experiment_id,
        filter_string=f"tags.mlflow.source.git.commit = '{get_git_sha()}'",
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=1,
        order_by=["metrics.accuracy ASC"],
    )
    best_run_id = best_runs[0].info.run_id
    return best_run_id


def download_model_artifacts(
    best_run_id: str, artifact_path: str = "model/model.pkl", dst_path: str = "."
) -> None:
    client = MlflowClient(tracking_uri=settings.MLFLOW_TRACKING_URI)
    Path(dst_path).mkdir(parents=True, exist_ok=True)
    client.download_artifacts(best_run_id, artifact_path, dst_path)


def load_model(model_path: Path) -> Pipeline:
    with open(model_path, "rb") as f:
        return pickle.load(f)
