from rest_framework import viewsets
from .models import Resident, Expense, DinnerClub, Debt, Credit, Payment, DinnerClubParticipant
from .serializers import ResidentSerializer, ExpenseSerializer, DinnerClubSerializer, DebtSerializer, CreditSerializer, PaymentSerializer, DinnerClubParticipantSerializer

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
