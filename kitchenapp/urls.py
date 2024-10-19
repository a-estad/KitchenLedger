# from django.contrib.auth.views import LoginView
# from django.contrib.auth import views as auth_views
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.front_page, name='front page'),
#     path('overview/', views.overview_page, name='overview page'),
#     path('expenses/', views.expenses_page, name='expenses page'),
#     path('dinner_clubs/', views.dinner_clubs_page, name='dinner clubs page'),
#     path('debt_and_credit/', views.debt_and_credit_page, name='debt and credit page'),
#     path('profile/<int:resident_id>', views.resident_profile, name='resident profile page')
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'residents', ResidentViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'dinnerclubs', DinnerClubViewSet)
router.register(r'debts', DebtViewSet)
router.register(r'credits', CreditViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'dinnerclubparticipants', DinnerClubParticipantViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
