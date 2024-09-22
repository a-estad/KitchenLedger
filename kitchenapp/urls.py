from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', views.front_page, name='front page'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path("accounting", views.accounting, name="accounting"),
]
