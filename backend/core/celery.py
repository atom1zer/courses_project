import os

from celery import Celery

if bool(os.getenv("DEBUG")):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.development")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.production")

app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
