from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.front_page, name='front page'),
    path('data/', views.data_tables, name='data tables page'),
    path('profile/<int:resident_id>', views.resident_profile, name='resident profile page')
]
