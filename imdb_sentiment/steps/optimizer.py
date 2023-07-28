import optuna
import pandas as pd
from optuna.integration.mlflow import MLflowCallback
from sklearn.metrics import accuracy_score

from imdb_sentiment.config.params import params
from imdb_sentiment.config.settings import settings

from .make_model import make_model

mlflc = MLflowCallback(
    tracking_uri=settings.MLFLOW_TRACKING_URI,
    metric_name="accuracy",
)


class Optimizer:
    def __init__(self, params: dict[str, any] = params):
        self.params = params["params"]

    def objective(
        self,
        trial: optuna.Trial,
        X_train: pd.DataFrame,
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

        model = make_model(param_space)
        model.fit(X_train, y_train)

        accuracy = accuracy_score(y_val, model.predict(X_val))

        return accuracy

    def optimize(
        self,
        X_train: pd.DataFrame,
        y_train: pd.DataFrame,
        X_val: pd.DataFrame,
        y_val: pd.DataFrame,
    ) -> optuna.trial.Trial:
        study = optuna.create_study(
            study_name=settings.EXPERIMENT_NAME, direction=params["direction"]
        )
        study.optimize(
            lambda trial: self.objective(trial, X_train, y_train, X_val, y_val),
            n_trials=params["n_trials"],
            callbacks=[mlflc],
            show_progress_bar=True,
        )
        return study.best_trial
