from django.contrib import admin
from .models import Teacher, Student, Task, TaskCategory, Solution


admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(TaskCategory)
admin.site.register(Task)
admin.site.register(Solution)
