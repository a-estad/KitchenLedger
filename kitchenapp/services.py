from django.db.models import Sum
from .signals import *
from .models import *


def recalculate_total_debt_for_resident(resident):
    debt = resident.debt_set.aggregate(Sum("amount", default=0.0))
    credit = resident.credit_set.aggregate(Sum("amount", default=0.0))
    deposit = resident.deposit_set.aggregate(Sum("amount", default=0.0))
    resident.total_debt = debt - credit - deposit
