from django import forms


class ExpenseForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',  # Bootstrap class for styling
            'id': 'dateInput',
            'type': 'date',
        }),
        required=True)
    cost = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',  # Bootstrap class for styling
            'id': 'costInput'
        }),
        required=True)
    description = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # Bootstrap class for styling
            'id': 'descriptionInput'
        }),
        max_length=100,
        required=True)
    is_dinner_club = forms
