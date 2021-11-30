FROM python:3.8

ENV POETRY_VERSION=1.0.10

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR usr/src/app

COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

CMD ["src/index.py"]
