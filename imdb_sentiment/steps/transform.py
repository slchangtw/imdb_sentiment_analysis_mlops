import re

BR_PATTERN = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")


def process_review(reviews: str) -> str:
    return BR_PATTERN.sub(" ", reviews.lower())


def convert_label(label: str) -> int:
    return 1 if label == "positive" else 0
