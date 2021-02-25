FROM python:3.8-slim

ENV APP_DIR /code
RUN mkdir -p $APP_DIR

RUN touch /tmp/jwt_fake_key
ENV JWT_SIGNING_KEY_FILE_PATH=/tmp/jwt_fake_key

WORKDIR $APP_DIR

RUN apt update && apt install -y postgresql libpq-dev python3-dev gcc libglib2.0-0 libgl1-mesa-glx

COPY requirements.txt $APP_DIR/
RUN pip install -q -r requirements.txt

COPY . $APP_DIR/
