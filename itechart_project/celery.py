import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itechart_project.settings')

app = Celery('itechart_project')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'sync-igdb-twice-a-day': {
        'task': 'main_app.tasks.sync_igdb_task',
        'schedule': crontab(hour=[0, 13])
    }
}
