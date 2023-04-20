import mlflow

from ml_projects.infrastructure.mlflow import init_mlflow

from .load_data import load_train_data
from .model import make_model


def train():
    init_mlflow()
    model = make_model()
    X_train, X_test, y_train, y_test = load_train_data()

    with mlflow.start_run():
        mlflow.sklearn.autolog()
        mlflow.set_tag("imdb", "0.0.1")
        model.fit(X_train, y_train)

        mlflow.log_metric("accuracy", model.score(X_test, y_test)) 
