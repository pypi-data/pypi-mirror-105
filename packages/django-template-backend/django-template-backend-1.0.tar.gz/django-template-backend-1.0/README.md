# Django Template Backend
A template for Django apps with support for Django REST Framework, filters, Celery tasks, Beat schedules tasks, pytest,
and other things.

## Setup
1. Install the project dependencies
````
$ pipenv install --dev
````

2. Refactor "template" names throughout project to desired name

3. Create models

4. Make migrations and migrate the database
```
$ pipenv run python manage.py makemigrations
$ pipenv run python manage.py migrate
```

5. Start the Django server
```
$ pipenv run python manage.py runserver
```

6. Optionally start the Celery related processes
```
$ redis-server
$ pipenv run celery -A template_project worker -l info
$ pipenv run celery -A template_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Tests
Tests are setup to run through Pytest. They can be invoked with:

```
$ pipenv run python manage.py test
```
or
```
$ pipenv run python -m pytest
```
