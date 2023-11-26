import os
import time

from celery import shared_task
from core.models import Solution, Task
from .utils import execute_sql_query
from django.core.files.base import ContentFile


@shared_task
def execute_sql_and_save_to_task(task_id):
    task = Task.objects.get(id=task_id)
    result = execute_sql_query(task.sql_query)
    time.sleep(2)
    csv_bytes = result.encode('utf-8')
    content_file = ContentFile(csv_bytes)

    file_path = os.path.join('task_' + f"{task.id}.csv")

    task.reference_file.save(file_path, content_file, save=True)

