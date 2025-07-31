#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

until source ./.venv/bin/activate
do
    echo "Waiting activate .venv ..."
done

until python manage.py makemigrations
do
    echo "Waiting for db apply changes..."
    sleep 2
done

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

# python manage.py collectstatic --noinput

# python manage.py createsuperuser --noinput

gunicorn core.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

# for debug
#python manage.py runserver 0.0.0.0:8000