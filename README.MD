# django-auth-microservice

Micro-service designed to perform identification, authentication and authorization.

## Prerequisites
 - Python 3.8
 - PostgreSQL
 - [microservice-email](https://github.com/DanielKusyDev/microservice-email)
 
## Usage

- Run required services
- Set environment variables or put them into `.env` file inside `core` directory. You can find variables in the `settings.py` file.
You can generate your SECRET_KEY by simple python command:
```
python -c 'import random; result = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]); print(result)'
```
- Migrate
```
python manage.py migrate
```
- Set DJANGO_SETTINGS_MODULE environment variable and run tests
 ```
 export DJANGO_SETTINGS_MODULE=core.settings # may differ due to the structure of the project files
 pytest
```
 - Run server
 ```
python manage.py runserver 0.0.0.0:8000
```

 - Visit swagger page at `/docs` to find all endpoints

![](https://imgur.com/bV2c2f5.jpg)
