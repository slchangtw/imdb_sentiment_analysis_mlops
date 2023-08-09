FROM python:3.9.16-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VIRTUALENVS_CREATE=false

COPY imdb_sentiment/ imdb_sentiment/
COPY model/ model/
COPY poetry.lock pyproject.toml ./

RUN pip install -U pip && \
    pip install poetry==1.5.1 && \
    poetry install --no-interaction --no-cache --without dev,test

EXPOSE 8000

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "imdb_sentiment.predict:app"]
