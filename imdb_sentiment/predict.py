import uvicorn
from fastapi import FastAPI

from imdb_sentiment.config.review import Review

from .steps import process_review
from .utils import load_model

app = FastAPI()
model = load_model("model/model.pkl")


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
