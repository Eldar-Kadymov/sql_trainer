import os
import time
from datetime import timedelta
from celery import shared_task
from core.models import Solution, Task
from teachers.utils import execute_sql_query
from django.core.files.base import ContentFile
import pandas as pd
import pytz
from django.utils import timezone


def compare_query_results(ideal_file, student_file):

    if not os.path.isfile(ideal_file):
        return f"Файл '{ideal_file}' не существует!"
    if not os.path.isfile(student_file):
        return f"Файл '{student_file}' не существует!"

    df_ideal = pd.read_csv(ideal_file, encoding='utf-8')
    df_student = pd.read_csv(student_file, encoding='utf-8')

    if not df_ideal.columns.equals(df_student.columns):
        return f"Структура данных отличается. Студент: {list(df_student.columns)}, Идеальный результат: {list(df_ideal.columns)}"
    elif len(df_ideal) != len(df_student):
        return f"Количество строк отличается. Студент: {len(df_student)}, Идеальный результат: {len(df_ideal)}"
    elif df_ideal.equals(df_student):
        return "Задание выполнено правильно!"
    else:
        try:
            diff = df_ideal.compare(df_student)
            return diff
        except ValueError as e:
            return f"Ошибка при сравнении данных: {e}"


@shared_task
def execute_sql_and_save_to_solution(solution_id):
    start_time = time.monotonic()

    solution = Solution.objects.get(id=solution_id)
    result = execute_sql_query(solution.query)
    csv_bytes = result.encode('utf-8')
    content_file = ContentFile(csv_bytes)

    task = solution.task

    moscow = pytz.timezone('Europe/Moscow')
    now = timezone.now()
    moscow_time = now.astimezone(moscow)
    formatted_time = moscow_time.strftime('%d.%m.%Y_%H-%M-%S')

    file_path = os.path.join('id_' + str(solution.student.id), 'task_' + str(task.id), f"{formatted_time}.csv")
    solution.result_file.save(file_path, content_file, save=True)

    end_time = time.monotonic()
    execution_time = timedelta(seconds=end_time - start_time)

    solution.execution_time = execution_time


    reference_file_path = task.reference_file.path
    student_file_path = solution.result_file.path

    comparison_result = compare_query_results(reference_file_path, student_file_path)

    if comparison_result == "Задание выполнено правильно!":
        solution.is_correct = True
    else:
        solution.is_correct = False
        solution.message = comparison_result

    solution.save()
