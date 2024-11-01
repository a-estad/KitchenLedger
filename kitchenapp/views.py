from rest_framework import viewsets, generics
from .models import Resident, Expense, DinnerClub, Debt, Credit, Payment, DinnerClubParticipant, Note
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user 
        return Note.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): # Find difference between get_queryset and setting queryset
        user = self.request.user 
        return Note.objects.filter(author=user)

class ResidentBalanceView(APIView):
    def get(self, request):
        residents_data = []

        for resident in Resident.objects.all():
            expensesPaidFor = Expense.objects.filter(paid_by=resident)
            totalPaidFor = expensesPaidFor.aggregate(total=Sum('cost'))['total'] or 0.0

            # Separate dinner club and non-dinner club expenses
            nonDinnerClubExpenses = Expense.objects.filter(paid_by=resident, is_dinner_club=False)
            dinnerClubExpenses = Expense.objects.filter(paid_by=resident, is_dinner_club=True)

            # Calculate totals
            nonDinnerClubTotal = nonDinnerClubExpenses.aggregate(total=Sum('cost'))['total'] or 0.0
            dinnerClubTotal = dinnerClubExpenses.aggregate(total=Sum('cost'))['total'] or 0.0

            # Populate resident data
            residents_data.append({
                "resident": resident.username,
                "paidFor": totalPaidFor,
                "non_dinner_club_total": nonDinnerClubTotal,
                "dinner_club_total": dinnerClubTotal,
                "balance": resident.balance,
            })

        return Response(residents_data)

class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    permission_classes = [AllowAny]
    authentication_classes = []      # Disables JWT authentication for this viewset

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()  # Add this line to set the queryset attribute

    def perform_create(self, serializer):
        serializer.save()

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
