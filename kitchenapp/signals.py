from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Expense, Resident, Credit, DinnerClub, DinnerClubParticipant

# Signal to update balance when an expense is created or updated
@receiver(post_save, sender=Expense)
def update_resident_balance_on_expense(sender, instance, created, **kwargs):
    resident = instance.paid_by
    residents = Resident.objects.all()

    if instance.is_dinner_club:
        # For dinner club expenses, get the specific participants
        dinner_club = DinnerClub.objects.get(expense=instance)
        dinner_club_participants = DinnerClubParticipant.objects.filter(dinner_club=dinner_club)
        debtors = [participant.resident for participant in dinner_club_participants]
    else:
        # For non-dinner club expenses, all residents are debtors
        debtors = residents

    # Calculate the per-person share of the expense
    share = instance.cost / len(debtors)

    # Subtract the share from each debtor
    for debtor in debtors:
        debtor.balance -= share
        debtor.save()

    # Add back the resident's share, so they only pay their portion
    resident.balance += instance.cost - share
    resident.save()


# Signal to update balance on credit creation
# @receiver(post_save, sender=Credit)
# def update_resident_balance_on_credit(sender, instance, created, **kwargs):
#     resident = instance.resident
#     resident.balance -= instance.amount  # Reduce balance by credit amount
#     resident.save()

# Signal to revert balance on expense deletion
@receiver(post_delete, sender=Expense)
def revert_balance_on_expense_delete(sender, instance, **kwargs):
    resident = instance.paid_by
    residents = Resident.objects.all()

    if instance.is_dinner_club:
        # For dinner club expenses, get the specific participants
        dinner_club = DinnerClub.objects.get(expense=instance)
        dinner_club_participants = DinnerClubParticipant.objects.filter(dinner_club=dinner_club)
        debtors = [participant.resident for participant in dinner_club_participants]
    else:
        # For non-dinner club expenses, all residents are debtors
        debtors = residents

    # Calculate the per-person share of the expense
    share = instance.cost / len(debtors)

    # Subtract the share from each debtor
    for debtor in debtors:
        debtor.balance += share
        debtor.save()

    # Add back the resident's share, so they only pay their portion
    resident.balance -= instance.cost - share
    resident.save()

