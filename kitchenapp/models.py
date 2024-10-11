from django.db import models
from django.contrib.auth.models import User


class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20)
    room_number = models.IntegerField()
    balance = models.FloatField()
    move_in_date = models.DateField()
    move_out_date = models.DateField()

    def __str__(self):
        return f"{self.room_number}: {self.name}"


class Expense(models.Model):
    paid_by = models.ForeignKey(Resident, on_delete=models.DO_NOTHING)
    date = models.DateField()
    cost = models.FloatField()
    is_dinner_club = models.BooleanField()
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"Expense {self.description} paid by {self.paid_by.name} on {self.date}"


class DinnerClub(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)

    def __str__(self):
        return f"DinnerClub at {self.expense.date}"


class DinnerClubParticipant(models.Model):
    dinner_club = models.ForeignKey(DinnerClub, on_delete=models.CASCADE)
    resident = models.ForeignKey(Resident, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.resident.name} participated in Dinner Club on {self.dinner_club.expense.date}"


class Debt(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.DO_NOTHING)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.resident.name} owes {self.amount} for {self.expense}"


class Credit(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.DO_NOTHING)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.resident.name} paid {self.amount} for {self.expense}"


class Payment(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.DO_NOTHING)
    date = models.DateField()
    amount = models.FloatField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} deposited by {self.resident.name} on {self.date}"
