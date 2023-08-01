import pickle

import pytest

from imdb_sentiment import process_review


@pytest.fixture(scope="session", name="model")
def fixture_model():
    with open("model/model.pkl", "rb") as f:
        return pickle.load(f)


@pytest.mark.parametrize(
    "review, label",
    [
        ("A nicely paced romantic war story that should have got more exposure.", 1),
        (
            (
                "The cinematography is the film's shining feature. Park really knows"
                "his stuff when it comes to shooting memorable scenes from behind a"
                "camera."
            ),
            1,
        ),
        (
            (
                "In 97 minutes of film we can only save one single idea,"
                "which was totally wasted in this movie I must say!"
            ),
            0,
        ),
        (
            (
                "The trouble with this film, like so many other films that fail,"
                "is the script."
            ),
            0,
        ),
    ],
)
def test_model_performance(model, review, label):
    processed_review = process_review(review)
    assert model.predict([processed_review])[0] == label
