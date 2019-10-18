FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /service
WORKDIR /service
COPY requirements.txt /service/
RUN pip install -r requirements.txt
COPY ./gematrix/ /service/
EXPOSE 8000
ENTRYPOINT ./manage.py runserver 0.0.0.0:8000
