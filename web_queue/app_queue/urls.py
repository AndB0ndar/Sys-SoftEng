from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    path('', views.home, name='home'),
    path('queues/', views.queues, name='queues'),
    path('queues/create', views.create_queue, name='create_queue'),
    path('queue/<int:pk>/', views.queue, name='queue'),
    path('queue/<int:pk>/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('queue/<int:pk>/add-user/<int:user_id>/', views.add_user, name='add_user'),
    path('queue/<int:pk>/update-user/<int:user_id>/', views.update_user, name='update_user'),
]
