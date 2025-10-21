from django.urls import path
from . import views

app_name = 'taskassignment'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Contributor URLs
    path('contributors/', views.contributor_list, name='contributor_list'),
    path('contributors/<int:pk>/', views.contributor_detail, name='contributor_detail'),
    path('contributors/create/', views.contributor_create, name='contributor_create'),
    path('contributors/<int:pk>/update/', views.contributor_update, name='contributor_update'),
    path('contributors/<int:pk>/delete/', views.contributor_delete, name='contributor_delete'),
    
    # Task URLs
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/toggle/', views.task_toggle_complete, name='task_toggle_complete'),
]
