from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signUp, name='signUp'),
    path('tasks/', views.tasks, name='tasks'),
    path('logout/', views.signOut, name='logout'),
    path('signin/', views.signIn, name='signin'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/task_detail/<int:task_id>/',
         views.task_detail, name='task_detail'),
    path('tasks/task_detail/<int:task_id>/completed',
         views.task_completed, name='task_completed'),
    path('tasks/task_detail/<int:task_id>/deleted',
         views.task_deleted, name='task_deleted'),
]
