from django.urls import path
from .views import add_task,view_task,deliver_task
app_name = "tasks"
urlpatterns = [
    path('', view_task, name='task_list'),
    path('update/<int:id>/', deliver_task, name='update_task'),
    path('add/', add_task, name='task_add'),
    # path('edit/<int:pk>/',edit_task, name='task_edit'),
    # path('delete/<int:pk>/', delete_task, name='task_delete'),
    # path('delete/<int:pk>/', complete_task, name='task_delete'),
]