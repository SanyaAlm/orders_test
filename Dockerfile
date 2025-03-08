FROM python:3.12

RUN apt-get update && apt-get install -y  \
    build-essential  \
    libpq-dev

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . /app
ENV PYTHONPATH=/app:/app
ENV PORT=8000
CMD ["sh", "-c", "alembic upgrade head && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]