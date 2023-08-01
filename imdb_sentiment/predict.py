import pickle

import uvicorn
from fastapi import FastAPI
from sklearn.pipeline import Pipeline

from .review import Review
from .steps.transform_data import process_review


def load_model() -> Pipeline:
    with open("model/model.pkl", "rb") as f:
        return pickle.load(f)


app = FastAPI()
model = load_model()


@app.get("/")
def index():
    return {"message": "IMDB Sentiment Analysis"}


@app.post("/predict")
async def predict_review(review: Review):
    review = review.model_dump()

    text = review["text"]
    processed_text = process_review(text)

    predict_label = model.predict([processed_text])
    sentiment = "positive" if predict_label[0] == 1 else "negative"

    return {"sentiment": sentiment}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
