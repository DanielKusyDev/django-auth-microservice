#!/bin/bash


echo "Waiting for db"
until PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST --user $DB_USER -c '\q'; do
  echo "PostgreSQL unavailable (code=$?)"
  sleep 1
done

echo "Db is up. Performing migrations and collecting static files..."

python manage.py migrate && python manage.py collectstatic --no-input

echo "Running server"
python manage.py runserver 0.0.0.0:8000