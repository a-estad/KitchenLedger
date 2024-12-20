from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Resident(AbstractUser):
    name = models.CharField(max_length=20)
    room_number = models.IntegerField(null=True)
    balance = models.FloatField(default=0.0)
    move_in_date = models.DateField(null=True)
    move_out_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.room_number}: {self.name}"

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # Automatically populate
    author = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title

class Expense(models.Model):
    paid_by = models.ForeignKey(Resident, on_delete=models.DO_NOTHING)  # Each expense belongs to one resident
    date = models.DateField()
    cost = models.FloatField()
    is_dinner_club = models.BooleanField(default=False)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"Expense {self.description} paid by {self.paid_by.name} on {self.date}"


class DinnerClub(models.Model):
    expense = models.OneToOneField(Expense, on_delete=models.DO_NOTHING)  # Each DinnerClub has one expense
    participants = models.ManyToManyField(Resident, through='DinnerClubParticipant')  # Many-to-many with residents

    def __str__(self):
        return f"DinnerClub at {self.expense.date}"


class DinnerClubParticipant(models.Model):
    dinner_club = models.ForeignKey(DinnerClub, on_delete=models.CASCADE)
    resident = models.ForeignKey(Resident, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.resident.name} participated in Dinner Club on {self.dinner_club.expense.date}"


class Debt(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.DO_NOTHING)  # Each debt belongs to one resident
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)  # Debt references one expense
    amount = models.FloatField()

    def __str__(self):
        return f"{self.resident.name} owes {self.amount} for {self.expense}"


class Credit(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.DO_NOTHING)  # Each credit belongs to one resident
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)  # Each credit references one expense
    amount = models.FloatField()

    def __str__(self):
        return f"{self.resident.name} paid {self.amount} for {self.expense}"


class Payment(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.DO_NOTHING)  # Each payment belongs to one resident
    date = models.DateField()
    amount = models.FloatField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} deposited by {self.resident.name} on {self.date}"
