from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from .models import Resident, Expense, Debt, Credit
from .forms import ExpenseForm
from .services import create_history_for_resident


@login_required
def front_page(request):
    residents = Resident.objects.all()
    return render(request, "kitchenapp/front_page.html", {'residents': residents})


def data_tables(request):
    all_expenses = Expense.objects.all()
    all_debts = Debt.objects.all()

    if request.method == 'POST':

        if 'expense_id_delete' in request.POST:
            expense_id_delete = request.POST.get('expense_id_delete')
            Expense.objects.get(pk=expense_id_delete).delete()
            form = ExpenseForm()

        else:
            form = ExpenseForm(request.POST)

            if form.is_valid():
                expense_input = form.cleaned_data
                expense = Expense(paid_by=request.user.resident,
                                  date=expense_input.get('date'),
                                  cost=expense_input.get('cost'),
                                  is_dinner_club=False,
                                  description=expense_input.get('description'))
                expense.save()

    else:
        form = ExpenseForm()

    return render(request, "kitchenapp/data_tables.html", {'form': form, 'expenses': all_expenses, 'debts': all_debts, 'resident': request.user.resident})


def expenses_page(request):
    all_expenses = Expense.objects.all()
    all_debts = Debt.objects.all()

    if request.method == 'POST':

        if 'expense_id_delete' in request.POST:
            expense_id_delete = request.POST.get('expense_id_delete')
            Expense.objects.get(pk=expense_id_delete).delete()
            form = ExpenseForm()

        else:
            form = ExpenseForm(request.POST)

            if form.is_valid():
                expense_input = form.cleaned_data
                expense = Expense(paid_by=request.user.resident,
                                  date=expense_input.get('date'),
                                  cost=expense_input.get('cost'),
                                  is_dinner_club=False,
                                  description=expense_input.get('description'))
                expense.save()

    else:
        form = ExpenseForm()

    return render(request, "kitchenapp/expenses.html", {'form': form, 'expenses': all_expenses, 'debts': all_debts, 'resident': request.user.resident})


def debt_and_credit_page(request):
    all_debts = Debt.objects.all()
    all_credits = Credit.objects.all()

    return render(request, "kitchenapp/debt_and_credit.html", {'debts': all_debts, 'credits': all_credits})

def resident_profile(request, resident_id):
    resident_for_profile = Resident.objects.get(pk=resident_id)

    history_table = sorted(create_history_for_resident(resident_for_profile), reverse=True)

    return render(request, "kitchenapp/resident_profile.html", {'resident': resident_for_profile, 'history': history_table})
