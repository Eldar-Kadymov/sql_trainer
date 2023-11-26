import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from slugify import slugify


# Модель пользователя
class BasePerson(models.Model):
    class Meta:
        abstract = True

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))

    email = models.EmailField(verbose_name=_('Электронная почта'))
    first_name = models.CharField(max_length=100, verbose_name=_('Имя'))
    last_name = models.CharField(max_length=100, verbose_name=_('Фамилия'))
    middle_name = models.CharField(max_length=100, verbose_name=_('Отчество'))

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    @property
    def short_name(self):
        return f'{self.last_name} {self.first_name[0]}. {self.middle_name[0]}.'

    def __str__(self):
        return self.full_name


# Модель преподавателя
class Teacher(BasePerson):
    class Meta:
        verbose_name = _('Преподаватель')
        verbose_name_plural = _('Преподаватели')

    @property
    def is_teacher(self):
        return True

    def __str__(self):
        return f'{self.full_name}'


# Модель студента
class Student(BasePerson):
    class Meta:
        verbose_name = _('Студент')
        verbose_name_plural = _('Студенты')

    @property
    def is_student(self):
        return True

    def __str__(self):
        return f'{self.full_name}'


# Модель раздела заданий
class TaskCategory(models.Model):
    name = models.CharField(max_length=100)


# Модель задания
class Task(models.Model):
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE)

    description = models.TextField()
    sql_query = models.TextField()
    reference_file = models.FileField(upload_to='solutions/')


# Модель попытки
class Solution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    query = models.TextField()
    execution_time = models.DurationField(null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    result_file = models.FileField(upload_to='student_results/')
    message = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(null=True, blank=True, default=None)

    @property
    def formatted_execution_time(self):
        if self.execution_time is None:
            return None

        total_milliseconds = self.execution_time.total_seconds() * 1000
        if total_milliseconds < 1000:
            return f"{total_milliseconds:.0f} ms"
        else:
            total_seconds = self.execution_time.total_seconds()
            return f"{total_seconds:.3f} s"
