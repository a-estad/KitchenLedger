from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Resident, Expense, Debt, Credit, DinnerClub, DinnerClubParticipant
from .forms import ExpenseForm
from .services import create_history_for_resident, create_debt_and_credit_for_expense, recalculate_debt_and_credit_for_expense


@login_required
def front_page(request):
    residents = Resident.objects.all()
    return render(request, "kitchenapp/front_page.html", {'residents': residents})


def overview_page(request):
    residents = sorted(Resident.objects.all(), key=lambda x: x.room_number)
    return render(request,
                  "kitchenapp/overview_page.html",
                  {'residents': residents})


def expenses_page(request):
    all_expenses = sorted(Expense.objects.filter(is_dinner_club=False), key=lambda x: x.date, reverse=True)
    current_user = request.user.resident

    if request.method == 'POST':

        if 'expense_id_delete' in request.POST:
            expense_id_delete = request.POST.get('expense_id_delete')
            Expense.objects.get(pk=expense_id_delete).delete()

            return redirect('expenses page')

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
                create_debt_and_credit_for_expense(expense)

                return redirect('expenses page')

    else:
        form = ExpenseForm()

    return render(request,
                  "kitchenapp/expenses.html",
                  {'form': form, 'expenses': all_expenses, 'resident': current_user})


def dinner_clubs_page(request):
    all_dinner_club_expenses = sorted(Expense.objects.filter(is_dinner_club=True).prefetch_related('dinnerclub__dinnerclubparticipant_set__resident'), key=lambda x: x.date, reverse=True)
    current_user = request.user.resident

    if request.method == 'POST':

        if 'dinner_club_expense_id_delete' in request.POST:
            dinner_club_expense_id= request.POST.get('dinner_club_expense_id_delete')
            Expense.objects.get(pk=dinner_club_expense_id).delete()

            return redirect('dinner clubs page')

        elif 'add_remove_participant_from_expense_id' in request.POST:
            dinner_club_expense_id = request.POST.get('add_remove_participant_from_expense_id')
            dinner_club_expense = Expense.objects.get(pk=dinner_club_expense_id)
            dinner_club = DinnerClub.objects.get(expense=dinner_club_expense)

            try:
                participant = DinnerClubParticipant.objects.get(dinner_club=dinner_club, resident=current_user)
            except DinnerClubParticipant.DoesNotExist:
                participant = None

            if participant is not None:
                DinnerClubParticipant.objects.get(dinner_club=dinner_club, resident=current_user).delete()
            else:
                DinnerClubParticipant(dinner_club=dinner_club, resident=current_user).save()

            recalculate_debt_and_credit_for_expense(dinner_club_expense)

            return redirect('dinner clubs page')

        else:
            form = ExpenseForm(request.POST)

            if form.is_valid():
                expense_input = form.cleaned_data
                expense = Expense(paid_by=request.user.resident,
                                  date=expense_input.get('date'),
                                  cost=expense_input.get('cost'),
                                  is_dinner_club=True,
                                  description=expense_input.get('description'))
                expense.save()
                dinner_club = DinnerClub(expense=expense)
                dinner_club.save()
                DinnerClubParticipant(dinner_club=dinner_club, resident=expense.paid_by).save()
                create_debt_and_credit_for_expense(expense)

                return redirect('dinner clubs page')

    else:
        form = ExpenseForm()

    return render(request,
                  "kitchenapp/dinner_club_expenses.html",
                  {'form': form, 'dinner_club_expenses': all_dinner_club_expenses, 'resident': current_user})


def debt_and_credit_page(request):
    all_debts = sorted(Debt.objects.all(), key=lambda x: x.expense.date, reverse=True)
    all_credits = sorted(Credit.objects.all(), key=lambda x: x.expense.date, reverse=True)

    return render(request,
                  "kitchenapp/debt_and_credit.html",
                  {'debts': all_debts, 'credits': all_credits})


def resident_profile(request, resident_id):
    resident_for_profile = Resident.objects.get(pk=resident_id)

    history_table = sorted(create_history_for_resident(resident_for_profile), reverse=True)

    return render(request,
                  "kitchenapp/resident_profile.html",
                  {'resident': resident_for_profile, 'history': history_table})
