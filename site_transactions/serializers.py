from rest_framework import serializers
from .models import GeneralTransaction, CardDeposit


class GeneralTransactionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = GeneralTransaction
        fields = '__all__'
        read_only_fields = ['id']

class CardTransactionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CardDeposit
        fields = '__all__'
        read_only_fields = ['id']
