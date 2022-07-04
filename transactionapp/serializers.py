
from pyexpat import model
from rest_framework import serializers

from transactionapp.models import Balance, Transaction


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('amount', 'type', 'created_at')