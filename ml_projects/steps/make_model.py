from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, make_pipeline

SEED = 42


def make_model() -> Pipeline:
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2), sublinear_tf=True, max_features=20000
    )

    dimensionality_reducer = TruncatedSVD(
        n_components=100, n_iter=10, random_state=SEED
    )

    predictor = HistGradientBoostingRegressor(
        max_iter=1000, random_state=SEED, verbose=0
    )

    return make_pipeline(vectorizer, dimensionality_reducer, predictor)
