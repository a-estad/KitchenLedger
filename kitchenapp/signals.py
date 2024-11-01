from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Expense, Resident, Credit, DinnerClub, DinnerClubParticipant

# Signal to update balance when an expense is created or updated
@receiver(post_save, sender=Expense)
def update_resident_balance_on_expense(sender, instance, created, **kwargs):
    resident = instance.paid_by
    print("test")

    if instance.is_dinner_club:
        # Handle dinner club expenses
        participants = DinnerClubParticipant.objects.filter(dinner_club__expense=instance)
        per_person_cost = instance.cost / participants.count() if participants.exists() else 0

        for participant in participants:
            participant_resident = participant.resident
            participant_resident.balance -= per_person_cost  # Deduct the dinner club cost
            participant_resident.save()

        # Add the full cost back to the resident who paid
        resident.balance += instance.cost
    else:
        # Handle non-dinner club expenses
        resident.balance += instance.cost

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

    if instance.is_dinner_club:
        participants = DinnerClubParticipant.objects.filter(dinner_club__expense=instance)
        per_person_cost = instance.cost / participants.count() if participants.exists() else 0

        for participant in participants:
            participant_resident = participant.resident
            participant_resident.balance += per_person_cost  # Add back the dinner club cost
            participant_resident.save()

        # Remove the full cost from the resident who paid
        resident.balance -= instance.cost
    else:
        # For regular expenses, subtract the cost from the balance
        resident.balance -= instance.cost

    resident.save()

