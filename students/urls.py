from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


app_name = 'students'

urlpatterns = [
    path('category_task_detail/<int:task_id>/', views.category_task_detail, name='category_task_detail'),
    path('get_solution_status/<int:solution_id>/', views.get_solution_status, name='get_solution_status'),
    path('submit_solution/', views.submit_solution, name='submit_solution'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
