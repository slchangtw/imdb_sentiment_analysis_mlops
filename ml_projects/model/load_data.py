from pathlib import Path
from typing import Iterable

from sklearn.model_selection import train_test_split

SEED = 42
LABEL_MAPPING = {"pos": 1, "neg": 0}
TRAIN_DATA_FOLDER = Path("data/imdb/train")


def load_train_data() -> tuple[Iterable, Iterable, Iterable, Iterable]:
    X = []
    y = []

    for label in LABEL_MAPPING.keys():
        text_folder = TRAIN_DATA_FOLDER / label
        for file_path in text_folder.rglob("*.txt"):
            with open(file_path, "r") as f:
                X.append(f.read())
                y.append(LABEL_MAPPING[label])

    return train_test_split(X, y, test_size=0.2, random_state=SEED)
