.PHONY: run migrate load dump static app check celery apikey

run:
	python manage.py runserver 0:8000

migrate:
	python manage.py makemigrations && python manage.py migrate

load:
	python manage.py loaddata ./fixtures/*.json

dump:
	python manage.py dumpdata $(model) --indent 4 > ./fixtures/$(model).json

static:
	python manage.py collectstatic --noinput

app:
	mkdir -p apps/$(name) && python manage.py startapp --template=./static/app_template.zip $(name) apps/$(name)

check:
	python manage.py check

apikey:
	python manage.py create_api_key $(name)

celery:
	python -m celery -A core worker -l info --detach
