FROM python:3.8.4-slim

ENV APP_DIR /app

RUN mkdir $APP_DIR
WORKDIR $APP_DIR

RUN apt update && apt install -y postgresql libpq-dev python3-dev gcc libglib2.0-0 libgl1-mesa-glx

COPY requirements.txt $APP_DIR/
RUN pip install -q -r requirements.txt
