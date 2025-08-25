








# Use official Python image
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN pip install poetry==1.8.2

RUN poetry install --with dev

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]








