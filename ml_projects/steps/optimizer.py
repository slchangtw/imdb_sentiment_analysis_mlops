import mlflow
import optuna
from optuna.integration.mlflow import MLflowCallback
import pandas as pd
from sklearn.metrics import log_loss

from config.settings import MLFLOW_TRACKING_URI
from config.params import params
from .make_model import make_model


mlflc = MLflowCallback(
    tracking_uri=MLFLOW_TRACKING_URI,
    metric_name=params["metric"],
)


class Optimizer:
    def __init__(self, params: dict[str, any]=params):
        self.params = params["param"]

    @mlflc.track_in_mlflow()
    def objective(
        self,
        trial: optuna.Trial,
        X_train: pd.Dataframe,
        y_train: pd.DataFrame,
        X_val: pd.DataFrame,
        y_val: pd.DataFrame,
    ) -> float:
        param_space = {}

        if int_params := self.params.get("int"):
            for k, v in int_params.items():
                suggested = trial.suggest_int(k, v["low"], v["high"])
                param_space.update({k: suggested})

        if float_params := self.params.get("float"):
            for k, v in float_params.items():
                suggested = trial.suggest_float(k, v["low"], v["high"], log=v["log"])
                param_space.update({k: suggested})

        model = make_model(**param_space)
        model.fit(X_train, y_train)

        loss_val = log_loss(y_val, model.predict(X_val), squared=False)

        mlflow.log_params(params)
        mlflow.log_metric(params["metric"], loss_val)

        return loss_val

    def optimize(
        self,
        X_train: pd.DataFrame,
        y_train: pd.DataFrame,
        X_val: pd.DataFrame,
        y_val: pd.DataFrame,
    ) -> optuna.trial.Trial:
        study = optuna.create_study(direction=params["direction"])
        study.optimize(
            lambda trial: self.objective(trial, X_train, y_train, X_val, y_val),
            n_trials=params["n_trials"],
            show_progress_bar=True,
        )
        return study.best_trial
