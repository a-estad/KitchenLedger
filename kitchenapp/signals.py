from django.db.models.signals import post_save
from django.dispatch import receiver
from .services import *
from .models import *


@receiver(post_save, sender=Expense)
def create_debt_and_credit_for_expense(sender, instance, **kwargs):
    creditor = instance.paid_by
    Credit.objects.create(resident=creditor, expense=instance, amount=instance.cost)

    if instance.is_dinner_club:
        dinner_club_for_expense = DinnerClub.objects.get(expense=instance.id)
        dinner_club_participants = DinnerClubParticipant.objects.get(dinner_club=dinner_club_for_expense)
        debtors = Resident.objects.filter(id__in=dinner_club_participants)
    else:
        debtors = Resident.objects.all()

    for debtor in debtors:
        Debt.objects.create(resident=debtor, expense=instance, amount=instance.cost / len(debtors))


@receiver(post_save, sender=Payment)
@receiver(post_save, sender=Credit)
@receiver(post_save, sender=Debt)
def update_total_debt_for_resident(sender, instance, **kwargs):
    recalculate_balance_for_resident(instance.resident)
