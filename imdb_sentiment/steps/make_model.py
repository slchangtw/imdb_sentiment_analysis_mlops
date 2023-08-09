from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, make_pipeline

SEED = 42


def make_model(params: dict[str, any]) -> Pipeline:
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english",
        sublinear_tf=True,
        max_features=20000,
    )

    dimensionality_reducer = TruncatedSVD(
        n_components=200, n_iter=10, random_state=SEED
    )

    predictor = HistGradientBoostingClassifier(random_state=SEED, verbose=0, **params)

    return make_pipeline(vectorizer, dimensionality_reducer, predictor)
