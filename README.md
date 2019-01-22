# django-project
```
pip3 install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py populate_db
python manage.py createsuperuser

docker-compose run --rm web python manage.py createsuperuser
docker-compose run --rm web python python manage.py collectstatic --noinput

heroku run python manage.py ...
```