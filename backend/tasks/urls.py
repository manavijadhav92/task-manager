from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('tasks/', views.get_tasks),
    path('tasks/create/', views.create_task),
    path('tasks/update/<int:id>/', views.update_task),
    path('tasks/delete/<int:id>/', views.delete_task),
]
