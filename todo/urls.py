from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), #done
    path('register/', views.register, name='register'), #done
    path('login/', views.user_login, name='login'), #done
    path('logout/', views.user_logout, name='logout'), #done
    path('tasks/', views.task_list, name='task_list'), #done
    path('tasks/create/', views.task_create, name='task_create'), #done
    path('tasks/update/<int:task_id>/', views.task_update, name='task_update'), #done
    path('tasks/delete/<int:task_id>/', views.task_delete, name='task_delete'), #done
]
