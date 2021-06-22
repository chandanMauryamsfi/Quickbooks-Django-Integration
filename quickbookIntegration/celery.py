import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickbookIntegration.settings')

app = Celery('quickbookIntegration' , backend='rpc://')


app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'fetching-QB-data' : {
        'task' : 'App.tasks.fetch',
        'schedule' : crontab(minute=0 , hour=0),
    }
}

app.conf.beat_schedule = {
    'fetching-QB-data' : {
        'task' : 'App.tasks.refresh_token',
        'schedule' : crontab(minute='*/57' , hour='*'),
    }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')