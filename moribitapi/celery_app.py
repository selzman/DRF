# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moribitapi.settings')

app = Celery('moribitapi')
broker_connection_retry_on_startup = True


app.config_from_object('django.conf:settings', namespace='CELERY')


CELERY_BROKER_URL = 'redis://localhost:6379/0'


app.conf.beat_schedule = {
    'reset-userdaily-every-midnight': {
        'task': 'Moribit_Module.tasks.reset_user_daily',
        'schedule': crontab(hour=0, minute=0),
        # 'schedule': crontab(minute='*/1'),
    },
}

app.conf.beat_schedule = {
    'reset-userdaily-every-midnight': {
        'task': 'Moribit_Module.tasks.delete_old_chats',
        'schedule': crontab(hour=0, minute=0),
        # 'schedule': crontab(minute='*/1'),
    },
}




# Terminal 1: Run Celery worker
# 

# Terminal 2: Run Celery Beat
# celery -A moribitapi beat --loglevel=info
# celery -A moribitapi worker -P solo --loglevel=info



app.autodiscover_tasks()
