# django-auth-microservice

Micro-service designed to perform identification, authentication and authorization.

## General structure
The application consists of one `users` CRUD module. It's meant to provide a straightforward interface for managing users including features like groups management, login & logout and retrieving lost password.
Models are simple, just extended version of built-in `AbstractUser` with additional field for date of suspension. Urls namespace includes endpoints for user & staff management, groups and passwords.

## Users
Groups are implemented in two ways. There are two basic groups - regular users and staff administrators. Administrators have practically non-limited access for every operation in the system however this can be customised. 
Users also can be assigned to customised groups available from API level. Interfaces for both users and groups are in form of CRUD endpoints.

## Permissions
Permissions are granted by [django-rules](https://github.com/dfunckt/django-rules) and defined inside `rules.py`. To restrict the access to given endpoint one needs to define such dictionary inside each class.
```python
permission_required = {
    "create": "allow_any",
    "update": "is_account_owner",
    "partial_update": "is_account_owner",
    "destroy": "users.delete",
}
```
Please visit `django-rules` repository for more details.

## Login & Logout
Authentication is provided by JSON Web Token standard. To obtain new JWT token the `/token/` endpoint needs to be visited with user data in request's body. The view will respond with both access and refresh token.
The library used here is [DRF Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/). Using external library has given the ability to specify the signing/verification algorithm. Check out the documentation for more details.

## Retrieving lost password
To retrieve the lost password there is need to attach one more service to the application. To send an email with a reset password token the application is using an email service with REST interface. It can be 
any application that takes email data and sends an email on sender's behave. The one used here is [this one](https://github.com/savsgio/microservice-email) made 
by [Sergio Andrés Virviescas Santana](https://github.com/savsgio). The part responsible for this feature is `ResetPasswordService` which in fact is a hook that fires on 
user requesting a new password.

## API Documentation
API is documented in form of Swagger schema. See `/docs` for all endpoints.

| ![](https://imgur.com/bV2c2f5.jpg) |
| :---: |

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
 
## Environment Variables
| NAME                        | TYPE   | REQUIRED | DEFAULT   |
|-----------------------------|--------|----------|-----------|
| SECRET_KEY                  | string | X        | N/A       |
| DEBUG                       | bool   |          | false     |
| ALLOWED_HOSTS               | list   | X        | N/A       |
| DB_DRIVER                   | string | X        | N/A       |
| DB_NAME                     | string | X        | N/A       |
| DB_USER                     | string |          | N/A       |
| DB_PASSWORD                 | string |          | N/A       |
| DB_PORT                     | number |          | N/A       |
| DB_HOST                     | string |          | N/A       |
| CORS_ALLOWED_ORIGINS        | list   |          | N/A       |
| MAILING_URL                 | string |          | N/A       |
| JWT_ALGORITHM               | string | X        | HS256     |
| JWT_SIGNING_KEY_FILE_PATH   | string | X        | N/A       |
| JWT_VERIFYING_KEY_FILE_PATH | string |          | N/A       |
| BASE_API_URL                | string |          | auth/api/ |
