# dan-auth

## Prerequisites
 - Python 3.8
 - pip
 
## Usage

 - Run Postgres
 - Add `local_settings.py` inside `core` directory.
 - Generate secret key:
```
python -c 'import random; result = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]); print(result)'
```
 - Fill `local_settings.py` with given secret key and your db settings if they are different than those in main settings
  file.
 
 - Run server
 ```
python manage.py runserver
```