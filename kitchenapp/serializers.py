from rest_framework import serializers

from kitchenapp.signals import adjust_balances_for_dinner_club
from .models import *
from django.contrib.auth.models import User

class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}} # Accept password when creating a user, but don't return password when serializing. 
    
    def create(self, validated_data):
        res = Resident.objects.create_user(**validated_data)
        return res
    
    def update(self, instance, validated_data):
        if "password" in validated_data:
            # Use set_password to hash and set the password securely
            instance.set_password(validated_data.pop("password"))
        return super().update(instance, validated_data)

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        ekstra_kwargs = {"author": {"read_only": True}}

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['paid_by']  # Prevent 'paid_by' from being manually set in the request

    def create(self, validated_data):
        validated_data['paid_by'] = self.context['request'].user
        return super().create(validated_data)

class DinnerClubSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    expense = ExpenseSerializer()
    participants = ResidentSerializer(source='participants.all', many=True, read_only=True)  # Add participants

    participantsRoomNumbers = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )

    class Meta:
        model = DinnerClub
        fields = ['id', 'expense', 'participantsRoomNumbers', 'participants']

    def create(self, validated_data):
        expense_data = validated_data.pop('expense')
        room_numbers = validated_data.pop('participantsRoomNumbers')

        participants = Resident.objects.all()
        # participants = Resident.objects.filter(room_number__in=room_numbers)
        # TODO: Check that the resident that paid is also in room_numbers
        # if participants.count() != len(room_numbers):
        #     raise serializers.ValidationError("One or more room numbers are invalid.")

        expense_serializer = ExpenseSerializer(data=expense_data, context=self.context)
        expense_serializer.is_valid(raise_exception=True)
        expense = expense_serializer.save()  # This will set 'paid_by' to the current user

        dinner_club = DinnerClub.objects.create(expense=expense)

        for resident in participants:
            DinnerClubParticipant.objects.create(dinner_club=dinner_club, resident=resident)

        # dinner_club.participants.set(participants)
        adjust_balances_for_dinner_club(expense=expense, operation='add')
        return dinner_club

class DinnerClubParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = DinnerClubParticipant
        fields = '__all__'

class DebtSerializer(serializers.ModelSerializer):
    expense = ExpenseSerializer(read_only=True)
    
    class Meta:
        model = Debt
        fields = '__all__'

class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


