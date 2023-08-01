import mlflow
import optuna
import pandas as pd
from optuna.integration.mlflow import MLflowCallback
from sklearn.metrics import accuracy_score

from imdb_sentiment.config.params import params
from imdb_sentiment.config.settings import settings

from .make_model import make_model

mlflc = MLflowCallback(
    tracking_uri=settings.MLFLOW_TRACKING_URI, metric_name="accuracy"
)


def make_param_space(trial: optuna.Trial) -> dict[str, any]:
    params_cadidates = params["params"]
    param_space = {}

    if int_params := params_cadidates.get("int"):
        for k, v in int_params.items():
            suggested = trial.suggest_int(k, v["low"], v["high"])
            param_space.update({k: suggested})

    if float_params := params_cadidates.get("float"):
        for k, v in float_params.items():
            suggested = trial.suggest_float(k, v["low"], v["high"], log=v["log"])
            param_space.update({k: suggested})

    return param_space


@mlflc.track_in_mlflow()
def objective(trial: optuna.Trial) -> float:
    param_space = make_param_space(trial)

    model = make_model(param_space)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_val, model.predict(X_val))

    mlflow.sklearn.log_model(model, "model")
    mlflow.log_params(param_space)
    mlflow.log_metric("accuracy", accuracy)

    return accuracy


class Optimizer:
    def __init__(self, params: dict[str, any] = params):
        self.params = params["params"]

    def optimize(self, datasets: tuple[pd.DataFrame]) -> optuna.trial.Trial:
        # @mlflc.track_in_mlflow() can only take trial as the single argument
        # so we have to define datasets as global variables.
        # TODO: find a better way to pass datasets to objective function
        global X_train, y_train, X_val, y_val
        X_train, y_train, X_val, y_val = datasets

        study = optuna.create_study(
            study_name=settings.EXPERIMENT_NAME, direction=params["direction"]
        )
        study.optimize(
            objective,
            n_trials=params["n_trials"],
            callbacks=[mlflc],
            show_progress_bar=True,
        )
        return study.best_trial
