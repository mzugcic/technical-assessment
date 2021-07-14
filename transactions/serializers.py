from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from transactions.models import Operation

User = get_user_model()


class OperationSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Operation
        fields = [
            'transaction_id',
            'amount',
            'created',
            'type',
        ]

    def get_type(self, obj):
        return obj.get_type_display()


class TransactionSerializer(OperationSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Operation
        fields = OperationSerializer.Meta.fields + [
            'user_id',
        ]
        extra_kwargs = {
            'type': {'read_only': True},
        }

    @transaction.atomic
    def create(self, validated_data):
        user = get_object_or_404(User, id=validated_data['user_id'])
        amount = validated_data['amount']

        if amount > 0:
            transaction_type = Operation.PURCHASE
        else:
            transaction_type = Operation.REFUND

        obj = Operation.objects.create(
            user_id=user.id,
            transaction_id=validated_data['transaction_id'],
            amount=amount,
            created=timezone.now(),
            type=transaction_type
        )

        user.balance += amount * -1
        user.save()

        return obj

    def validate(self, data):
        user = get_object_or_404(User, id=data['user_id'])
        amount = data['amount']

        # Raise error if user is trying to spend more money than he owns
        if amount > 0 and user.balance < amount:
            raise ValidationError(
                f'You don\'t have sufficient funds for making a purchase. Your current balance is '
                f'{user.balance} GBP.'
            )

        return data


class WithdrawalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Operation
        fields = [
            'amount',
        ]

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user

        obj = Operation.objects.create(
            user_id=user.id,
            # Amount is multiplied by -1 so it turns into a negative number as intended
            amount=validated_data['amount'] * -1,
            created=timezone.now(),
            type=Operation.WITHDRAWAL
        )

        user.balance -= validated_data['amount']
        user.save()

        return obj

    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError(
                'Please enter the amount you wish to withdraw. It cannot be negative or 0.'
            )

        balance = self.context['request'].user.balance
        if balance < value:
            raise ValidationError(
                f'The amount you wish to withdraw exceeds your balance. Your current balance is '
                f'{balance} GBP.'
            )

        return value

    def to_representation(self, instance):
        return {'msg': 'Your withdrawal was successful.'}


class UserBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'balance',
        ]
