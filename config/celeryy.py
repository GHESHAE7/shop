from celery import Celery
import os
# from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("celery")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(related_name="tasks")


@app.task  # for celery test
def main():
    pass
