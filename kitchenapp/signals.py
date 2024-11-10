from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from .models import Expense, DinnerClub, DinnerClubParticipant, Resident, Debt

@receiver(post_save, sender=Expense)
def update_resident_balance_on_expense(sender, instance, created, **kwargs):
    if not instance.is_dinner_club:
        adjust_balances_for_expense(expense=instance, operation='add')


@receiver(post_delete, sender=Expense)
def revert_balance_on_expense_delete(sender, instance, **kwargs):
    if not instance.is_dinner_club:
        adjust_balances_for_expense(expense=instance, operation='subtract')

@receiver(pre_delete, sender=DinnerClub)
def revert_balance_on_dinner_club_deletion(sender, instance, **kwargs):
    adjust_balances_for_dinner_club(instance.expense, operation='subtract')


def adjust_balances_for_expense(expense: Expense, operation: str):
    residentThatPaid = expense.paid_by
    residents = (
        (Resident.objects.filter(move_out_date__gt=expense.date, move_in_date__lt=expense.date) |
         Resident.objects.filter(move_in_date__isnull=True)) &
        Resident.objects.filter(is_superuser=False)
    ).distinct()

    share = expense.cost / len(residents)

    for resident in residents:
        if resident != residentThatPaid:
            if operation == 'add':
                Debt.objects.create(resident=resident, expense=expense, amount=share)
                resident.balance -= share
            elif operation == 'subtract':
                resident.balance += share
            resident.save()

    if operation == 'add':
        Debt.objects.create(resident=residentThatPaid, expense=expense, amount=share)
        residentThatPaid.balance += expense.cost - share
    elif operation == 'subtract':
        residentThatPaid.balance -= expense.cost - share
    residentThatPaid.save()


def adjust_balances_for_dinner_club(expense: Expense, operation: str):
    residentThatPaid = expense.paid_by
    dinner_club = DinnerClub.objects.get(expense=expense)
    participants = [participant.resident for participant in DinnerClubParticipant.objects.filter(dinner_club=dinner_club)]

    share = expense.cost / len(participants)
    for participant in participants:
        if participant != residentThatPaid:
            if operation == 'add':
                Debt.objects.create(resident=participant, expense=expense, amount=share)
                participant.balance -= share
            elif operation == 'subtract':
                participant.balance += share
            participant.save()

    if operation == 'add':
        Debt.objects.create(resident=residentThatPaid, expense=expense, amount=share)
        residentThatPaid.balance += expense.cost - share
    elif operation == 'subtract':
        residentThatPaid.balance -= expense.cost - share
        print(expense.is_dinner_club)
        expense.delete()
    residentThatPaid.save()
