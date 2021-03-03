# pull official base image
FROM python:3.8

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt update && apt install -y postgresql gcc python3-dev musl-dev libglib2.0-0 libgl1-mesa-glx libpq-dev

RUN touch /tmp/jwt_fake_key
ENV JWT_SIGNING_KEY_FILE_PATH=/tmp/jwt_fake_key

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

