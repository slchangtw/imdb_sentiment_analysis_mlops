from pathlib import Path

import mlflow
import optuna
from config.settings import MLFLOW_TRACKING_URI
from make_model import make_model
from optuna.integration.mlflow import MLflowCallback
from sklearn.metrics import log_loss

from .load_data import load_data
from .transform_data import convert_label, process_review

mlflc = MLflowCallback(
    tracking_uri=MLFLOW_TRACKING_URI,
    metric_name="rmse_val",
)


@mlflc.track_in_mlflow()
def objective(trial: optuna.Trial, X_train, y_train, X_val, y_val, params: dict) -> float:
    model = make_model(**params)
    model.fit(X_train, y_train)

    log_loss_val = log_loss(y_val, model.predict(X_val), squared=False)

    mlflow.log_params(params)
    mlflow.log_metric("log_loss_val", log_loss_val)
    return log_loss_val

def train(params: dict, train_data_path: Path, val_data_path: Path):
    train = load_data(train_data_path)
    val = load_data(val_data_path)

    train["text"] = train["review"].apply(process_review)
    val["text"] = val["review"].apply(process_review)
    train["label"] = train["sentiment"].apply(convert_label)
    val["label"] = val["sentiment"].apply(convert_label)

    X_train = train["text"]
    y_train = train["label"]
    X_val = val["text"]
    y_val = val["label"]

    study = optuna.create_study(direction="minimize")
    study.optimize(
        lambda trial: objective(trial, X_train, y_train, X_val, y_val, params),
        n_trials=100,
        callbacks=[mlflc],
    )

    best_trial = study.best_trial
    print(f"Best trial: {best_trial.value}")