from django.utils import timezone
from django.utils.formats import date_format
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
import pytz
from core.models import Solution, Task, TaskCategory
from .tasks import execute_sql_and_save_to_solution
from teachers.utils import execute_sql_query
from django.core.files.base import ContentFile
from django.views.decorators.http import require_POST
from .utils import format_date

def category_task_detail(request, task_id=1):
    categories = TaskCategory.objects.all()
    current_task = get_object_or_404(Task, pk=task_id)
    student = request.user.student
    solutions = Solution.objects.filter(task=current_task, student=student).order_by('-submission_date')

    tasks = Task.objects.all()

    categories_list = {}
    for category in categories:
        tasks = Task.objects.filter(category=category)
        tasks_status = {}
        for task in tasks:
            is_task_started = Solution.objects.filter(student=student, task=task).exists()

            if is_task_started:
                is_task_completed = Solution.objects.filter(student=student, task=task, is_correct=True).exists()
            else:
                is_task_completed = None

            tasks_status[task] = is_task_completed

        categories_list[category] = tasks_status


    context = {
        'categories': categories,
        'task': current_task,
        'solutions': solutions,
        'categories_list': categories_list
    }
    return render(request, 'students/category_task_detail.html', context)


def get_solution_status(request, solution_id):
    print(solution_id)
    solution = Solution.objects.get(id=solution_id)

    if solution.is_correct is None:
        status = "Запрос выполняется"
        execution_time = '-'
    elif solution.is_correct:
        status = "Верно"
        execution_time = solution.formatted_execution_time
    else:
        status = "Неверно"
        execution_time = solution.formatted_execution_time

    student = request.user.student

    task = solution.task
    is_task_started = Solution.objects.filter(student=student, task=task).exists()

    if is_task_started:
        task_status = Solution.objects.filter(student=student, task=task, is_correct=True).exists()
    else:
        task_status = None



    return JsonResponse({'status': status, 'task_status': task_status, 'execution_time':execution_time})

@require_POST
def submit_solution(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        student = request.user.student
        task_id = request.POST.get('task_id')

        task = Task.objects.get(pk=task_id)

        solution = Solution.objects.create(task=task, student=student, query=query)

        execute_sql_and_save_to_solution.delay(solution.id)

        return JsonResponse({
            'status': 'success',
            'solution_id': solution.id,
            'submission_date': format_date(solution.submission_date)
        })
    else:
        return JsonResponse({'status': 'error'})
