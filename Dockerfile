ARG PYTHON_VERSION=3.12.4
FROM python:${PYTHON_VERSION}-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src
EXPOSE 8085

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=8085"]