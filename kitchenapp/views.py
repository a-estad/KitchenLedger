from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from .models import Resident, Expense, Debt
from .forms import ExpenseForm


@login_required
def front_page(request):
    residents = Resident.objects.all()
    return render(request, "front_page.html", {'residents': residents})

def data_tables(request):
    all_expenses = Expense.objects.all()
    all_debts = Debt.objects.all()

    if request.method == "POST":
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

    return render(request, "data_tables.html", {'form': form, 'expenses': all_expenses, 'debts': all_debts})

# def resident_page(request):
#     resident = Resident.objects.get(user=request.user)
#     return render(request, 'resident_page.html', {'resident': resident})
#
#
# def accounting(request):
#     return HttpResponse("You are at the accounting page.")
