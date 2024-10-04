from django.db.models import Sum
from .signals import *
from .models import *


def recalculate_total_debt_for_resident(resident):
    debt = resident.debt_set.aggregate(total=Sum("amount", default=0.0)).get('total')
    credit = resident.credit_set.aggregate(total=Sum("amount", default=0.0)).get('total')
    payment = resident.payment_set.aggregate(total=Sum("amount", default=0.0)).get('total')
    resident.total_debt = debt - credit - payment
    resident.save()
