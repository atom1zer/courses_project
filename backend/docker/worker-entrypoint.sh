#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

until source ./.venv/bin/activate
do
    echo "Waiting activate .venv ..."
done

# run a worker :)
# python3 -m celery -A core worker -l info --detach
celery -A core worker --loglevel=info --concurrency 1 -E
