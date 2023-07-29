import pytest

from imdb_sentiment import convert_label, process_review


@pytest.mark.parametrize(
    "review, result",
    [
        ("<br /><br />test", " test"),
        ("a-b", "a b"),
        ("a/b", "a b"),
    ],
)
def test_process_review(review, result):
    assert process_review(review) == result


def test_convert_label():
    assert convert_label("positive") == 1
    assert convert_label("negative") == 0
