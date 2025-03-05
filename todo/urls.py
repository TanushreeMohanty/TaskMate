from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page ✅
    
    # Authentication URLs
    path('register/', views.register, name='register'),  # User registration ✅
    path('login/', views.user_login, name='login'),  # User login ✅
    path('logout/', views.user_logout, name='logout'),  # User logout ✅
    
    # Task Management URLs
    path('tasks/', views.task_list, name='task_list'),  # List all tasks ✅
    path('tasks/create/', views.task_create, name='task_create'),  # Create a new task ✅
    path('tasks/update/<int:task_id>/', views.task_update, name='task_update'),  # Update a task ✅
    path('tasks/delete/<int:task_id>/', views.task_delete, name='task_delete'),  # Delete a task ✅
]
