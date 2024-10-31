from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ["id", "username", "password"]
        extra_kware = {"passord": {"write_only": True}} # Accept password when creating a user, but don't return password when serializing. 
    
    def create(self, validated_data):
        res = Resident.objects.create_user(**validated_data) # understand **
        return res

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        ekstra_kwargs = {"author": {"read_only": True}}

class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['paid_by']  # Prevent 'paid_by' from being manually set in the request

    def create(self, validated_data):
        validated_data['paid_by'] = self.context['request'].user
        return super().create(validated_data)

class DinnerClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = DinnerClub
        fields = '__all__'

class DebtSerializer(serializers.ModelSerializer):
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

class DinnerClubParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = DinnerClubParticipant
        fields = '__all__'
