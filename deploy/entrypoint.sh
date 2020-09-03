#!/bin/bash
cd "$APP_DIR" && ./manage.py migrate && ./manage.py collectstatic --no-input && ./manage.py runserver 0.0.0.0:8000 2>&1