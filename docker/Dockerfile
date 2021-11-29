FROM python:3.10

LABEL maintainer="Boris El Gareh <elgarehb@gmail.com>"

ARG SA_KEY_FILE
COPY ${SA_KEY_FILE} /sa_key_file.json
ENV GOOGLE_APPLICATION_CREDENTIALS="/sa_key_file.json"

RUN apt-get update && apt-get install -y \
  ffmpeg \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./src/config/gunicorn_conf.py /gunicorn_conf.py
COPY ./src/scripts/start.sh /start.sh
COPY ./src/app /app

EXPOSE 80

CMD ["/start.sh"]