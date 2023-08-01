from pathlib import Path

from .load_data import load_data
from .optimizer import Optimizer
from .transform_data import convert_label, process_review


def train(train_data_path: str, val_data_path: str):
    train_data_path = Path(train_data_path)
    val_data_path = Path(val_data_path)
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

    optimizer = Optimizer()
    optimizer.optimize((X_train, y_train, X_val, y_val))


if __name__ == "__main__":
    train("data/train.csv", "data/valid.csv")
