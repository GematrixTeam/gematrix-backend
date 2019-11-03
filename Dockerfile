FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
RUN apk add --no-cache postgresql-dev
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    && pip install --no-cache-dir psycopg2 \
    && apk del --no-cache .build-deps
COPY requirements.txt /
RUN pip3 install -r requirements.txt
RUN mkdir /service
WORKDIR /service
COPY ./gematrix/ /service/
EXPOSE 8000
ENTRYPOINT ./manage.py runserver 0.0.0.0:8000
