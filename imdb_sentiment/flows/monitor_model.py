from pathlib import Path

import pandas as pd
from prefect import flow, task
from prefect_aws import S3Bucket

from imdb_sentiment.steps import process_review
from imdb_sentiment.utils import load_model


@task()
def fetch_files_from_s3(test_data_path: Path, model_path: Path) -> None:
    s3_bucket_block = S3Bucket.load("aws-s3")
    s3_bucket_block.download_object_to_path("model.pkl", model_path)
    s3_bucket_block.download_object_to_path("test.csv", test_data_path)


@task()
def read_data(data_path: Path) -> pd.DataFrame:
    return pd.read_csv(data_path)


@task()
def process_review_col(review_col: pd.Series) -> pd.Series:
    return review_col.apply(process_review)


@task()
def upload_predictions_s3(data_path) -> None:
    s3_bucket_block = S3Bucket.load("aws-s3")
    s3_bucket_block.upload_from_path(data_path, "test_prediction.csv")


@flow()
def monitor_model():
    monitor_files_folder = Path("monitor_files")
    monitor_files_folder.mkdir(exist_ok=True)

    test_data_path = monitor_files_folder / "test.csv"
    model_path = monitor_files_folder / "model.pkl"
    test_prediction_path = monitor_files_folder / "test_prediction.csv"

    fetch_files_from_s3(test_data_path, model_path)

    model = load_model(monitor_files_folder / "model.pkl")
    test_data = read_data(test_data_path)

    test_data["processed_review"] = process_review_col(test_data["review"])
    test_data["predicted_label"] = model.predict(test_data["processed_review"])
    test_data.to_csv(test_prediction_path, index=False)

    upload_predictions_s3(test_prediction_path)


if __name__ == "__main__":
    monitor_model()
