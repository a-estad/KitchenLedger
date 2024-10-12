from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.front_page, name='front page'),
    path('data/', views.data_tables, name='data tables page'),
    path('expenses/', views.expenses_page, name='expenses page'),
    path('debt_and_credit/', views.debt_and_credit_page, name='debt and credit page'),
    path('profile/<int:resident_id>', views.resident_profile, name='resident profile page')
]
