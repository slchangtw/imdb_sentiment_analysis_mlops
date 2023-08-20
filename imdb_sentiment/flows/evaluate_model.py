import pandas as pd
from sklearn.metrics import classification_report

from imdb_sentiment.steps import convert_label, process_review
from imdb_sentiment.utils import load_model


def print_classification_report() -> None:
    valid = pd.read_csv("data/valid.csv")
    model = load_model("model/model.pkl")

    valid["review"] = valid["review"].apply(process_review)
    valid["sentiment"] = valid["sentiment"].apply(convert_label)

    valid["predicted_label"] = model.predict(valid["review"])

    print(classification_report(valid["sentiment"], valid["predicted_label"]))


if __name__ == "__main__":
    print_classification_report()
