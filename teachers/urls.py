from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


app_name = 'teachers'

urlpatterns = [
    path('category_list/', views.category_list, name='category_list'),
    path('category_add/', views.category_add, name='category_add'),
    path('create_task/<int:category_id>', views.create_task, name='create_task'),
    path('task/<int:task_id>/', views.task_description, name='task_description'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)