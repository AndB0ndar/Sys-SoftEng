from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    path('', views.home, name='home'),
    path('queues/', views.queues, name='queues'),
    path('queues/<slug:title>', views.queue, name='queue'),
]