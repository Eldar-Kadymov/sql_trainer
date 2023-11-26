from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from core.forms import LoginForm
from core.models import Student, Teacher
from django.contrib.auth.models import User
from django.contrib import messages


def custom_login(request):
    error_message = None
    form = LoginForm()

    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Пользователя с таким логином не существует")
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if Student.objects.filter(user=user).exists():
                    return redirect('students:category_task_detail', task_id=1)
                elif Teacher.objects.filter(user=user).exists():
                    return redirect('teachers:category_list')
                else:
                    messages.error(request, "Пользователь не является студентом или преподавателем")
            else:
                messages.error(request, "Неправильный пароль")


    return render(request, 'core/login.html', {'form': form})
