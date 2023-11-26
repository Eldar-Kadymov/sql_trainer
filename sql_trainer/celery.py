# myproject/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sql_trainer.settings')

app = Celery('sql_trainer')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


CELERYD_HIJACK_ROOT_LOGGER = False
CELERYD_LOG_LEVEL = 'INFO'