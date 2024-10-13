from django.db.models import Sum
from .signals import *
from .models import *


def create_debt_and_credit_for_expense(expense):
    creditor = expense.paid_by
    Credit.objects.create(resident=creditor, expense=expense, amount=expense.cost)

    residents = Resident.objects.filter(move_in_date__lt=expense.date).filter(move_out_date__gt=expense.date)

    if expense.is_dinner_club:
        dinner_club = DinnerClub.objects.get(expense=expense)
        dinner_club_participants = DinnerClubParticipant.objects.filter(dinner_club=dinner_club)
        debtors = [dinner_club_participant.resident for dinner_club_participant in dinner_club_participants]
    else:
        debtors = residents

    for debtor in debtors:
        Debt.objects.create(resident=debtor, expense=expense, amount=expense.cost / len(debtors))

    for resident in residents:
        recalculate_balance_for_resident(resident)


def recalculate_debt_and_credit_for_expense(expense):
    Debt.objects.filter(expense=expense).delete()
    Credit.objects.filter(expense=expense).delete()

    create_debt_and_credit_for_expense(expense)


def recalculate_balance_for_resident(resident):
    debt = resident.debt_set.aggregate(total=Sum("amount", default=0.0)).get('total')
    credit = resident.credit_set.aggregate(total=Sum("amount", default=0.0)).get('total')
    payment = resident.payment_set.aggregate(total=Sum("amount", default=0.0)).get('total')
    resident.balance = - debt + credit + payment
    resident.save()


def create_history_for_resident(resident):
    history_expenses = list(map(lambda e: (e.date, f"{resident.name} paid {e.cost} for {e.description}"), resident.expense_set.filter(is_dinner_club=False)))
    history_debts = list(map(lambda d: (d.expense.date, f"{resident.name} owes {d.amount} for {d.expense.description}"), resident.debt_set.all()))
    history_payments = list(map(lambda p: (p.date, f"{resident.name} made a payment of {p.amount}"), resident.payment_set.all()))
    history_dinner_clubs = list(map(lambda e: (e.date, f"{resident.name} hosted a dinner club with {len(DinnerClubParticipant.objects.filter(dinner_club=DinnerClub.objects.get(expense=e)))} participants, which cost {e.cost}"), resident.expense_set.filter(is_dinner_club=True)))
    history_dinner_club_participations = list(map(lambda p: (p.dinner_club.expense.date, f"{resident.name} participated in a dinner club hosted by {p.dinner_club.expense.paid_by}"), resident.dinnerclubparticipant_set.all()))
    return history_expenses + history_debts + history_payments + history_dinner_clubs + history_dinner_club_participations
