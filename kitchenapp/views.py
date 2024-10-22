from rest_framework import viewsets, generics
from .models import Resident, Expense, DinnerClub, Debt, Credit, Payment, DinnerClubParticipant
from .serializers import ResidentSerializer, ExpenseSerializer, DinnerClubSerializer, DebtSerializer, CreditSerializer, PaymentSerializer, DinnerClubParticipantSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class DinnerClubViewSet(viewsets.ModelViewSet):
    queryset = DinnerClub.objects.all()
    serializer_class = DinnerClubSerializer

class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer

class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class DinnerClubParticipantViewSet(viewsets.ModelViewSet):
    queryset = DinnerClubParticipant.objects.all()
    serializer_class = DinnerClubParticipantSerializer
