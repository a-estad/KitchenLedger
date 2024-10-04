from django import forms


class ExpenseForm(forms.Form):
    date = forms.DateField()
    cost = forms.FloatField()
    description = forms.CharField(max_length=100)
    is_dinner_club = forms
