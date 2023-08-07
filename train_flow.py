import typer
from typing_extensions import Annotated

from imdb_sentiment import download_model_artifacts, get_best_run_id, train

app = typer.Typer()


@app.command()
def train_flow(
    train_data_path: Annotated[
        str, typer.Argument(help="Path to the training data")
    ] = "data/train.csv",
    val_data_path: Annotated[
        str, typer.Argument(help="Path to the validation data")
    ] = "data/valid.csv",
) -> None:
    train(train_data_path, val_data_path)
    best_run_id = get_best_run_id()
    download_model_artifacts(best_run_id)


if __name__ == "__main__":
    app()
