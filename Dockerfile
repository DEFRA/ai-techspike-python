ARG PYTHON_VERSION=3.12.4
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
  --disabled-password \
  --gecos "" \
  --home "/nonexistent" \
  --shell "/sbin/nologin" \
  --no-create-home \
  --uid "${UID}" \
  appuser

COPY ./requirements.txt /app/requirements.txt
COPY ./logging.yaml /app/logging.yaml

RUN --mount=type=cache,target=/root/.cache/pip \
  --mount=type=bind,source=requirements.txt,target=/app/requirements.txt \
  python -m pip install -r /app/requirements.txt

USER appuser

COPY ./src /app/src
EXPOSE 8085

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=8085", "--log-config", "/app/logging.yaml", "--no-access-log"]