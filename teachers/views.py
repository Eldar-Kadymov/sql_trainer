from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from core.models import Task, TaskCategory
from teachers.tasks import execute_sql_and_save_to_task
from teachers.utils import execute_sql_query
from django.core.files.base import ContentFile

def category_list(request):
    categories = TaskCategory.objects.all()

    context = {
        'categories': categories,
    }
    return render(request, 'teachers/category_list.html', context)


def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('category_name')
        if name:
            TaskCategory.objects.create(name=name)
            return redirect('teachers:category_list')

    return render(request, 'teachers/category_add.html')


def create_task(request, category_id):
    category = TaskCategory.objects.get(id=category_id)

    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        description = request.POST.get('description')
        sql_query = request.POST.get('sql_query')

        new_task = Task.objects.create(
            category=category,
            description=description,
            sql_query=sql_query
        )

        execute_sql_and_save_to_task.delay(new_task.id)

        return redirect('teachers:category_list')

    return render(request, 'teachers/create_task.html')


def task_description(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    file_content = ""
    if task.reference_file:
        with task.reference_file.open() as file:
            file_content = file.read().decode('utf-8')

    return render(request, 'teachers/task_description.html', {'task': task, 'file_content': file_content})
