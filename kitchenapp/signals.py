from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Debt, Expense, Resident, Credit, DinnerClub, DinnerClubParticipant

# Signal to update balance when an expense is created or updated
@receiver(post_save, sender=Expense)
def update_resident_balance_on_expense(sender, instance, created, **kwargs):
    adjust_balances_for_expense(expense=instance, operation='add')

# Signal to revert balance on expense deletion
@receiver(post_delete, sender=Expense)
def revert_balance_on_expense_delete(sender, instance, **kwargs):
    adjust_balances_for_expense(expense=instance, operation='subtract')

def adjust_balances_for_expense(expense: Expense, operation: str):
    """
    Adjust the balances for residents based on an expense.
    
    Parameters:
    - expense: The Expense instance being processed.
    - operation: A string, either 'add' or 'subtract', indicating the balance adjustment.
    """
    residentThatPaid = expense.paid_by
    residents = (
        (Resident.objects.filter(move_out_date__gt=expense.date, move_in_date__lt=expense.date, ) |
        Resident.objects.filter(move_in_date__isnull=True)) &
        Resident.objects.filter(is_superuser=False)
    ).distinct()

    if expense.is_dinner_club:
        dinner_club = DinnerClub.objects.get(expense=expense)
        dinner_club_participants = DinnerClubParticipant.objects.filter(dinner_club=dinner_club)
        debtors = [participant.resident for participant in dinner_club_participants]
    else:
        debtors = list(residents)

    share = expense.cost / len(debtors)
    debtors = [resident for resident in debtors if resident != residentThatPaid]

    for debtor in debtors:
        if operation == 'add':
            Debt.objects.create(resident=debtor, expense=expense, amount=share)
            debtor.balance -= share
        elif operation == 'subtract':
            debtor.balance += share
        debtor.save()

    if operation == 'add':
        Debt.objects.create(resident=residentThatPaid, expense=expense, amount=share)
        residentThatPaid.balance += expense.cost - share
    elif operation == 'subtract':
        residentThatPaid.balance -= expense.cost - share
    residentThatPaid.save()

