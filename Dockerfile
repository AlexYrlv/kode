FROM python:3.12-slim

RUN pip install --no-cache-dir poetry

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-root

COPY . /app

CMD ["python", "manage.py"]
