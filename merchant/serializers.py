from rest_framework import serializers
from .models import MerchantBuyingRate
from django.conf import settings
import re


class MerchantBuyingRateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MerchantBuyingRate
        fields = '__all__'
        read_only_fields = ['id']


class ProcessingTransactionSerializer(serializers.Serializer):
    buyers_quantity = serializers.IntegerField()
    merchant_id = serializers.IntegerField()
    payment_method = serializers.IntegerField(default=0)  # default is wallet which is 0 and card is 1
    trading_currency = serializers.CharField(default="USD")

    def validate_buyers_quantity(self, value):
        # Check if the quantity is less than or equal to zero
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate_trading_currency(self, value):
        # Check if the provided currency is in the list of valid currency codes from settings.py
        if value not in settings.VALID_CURRENCY_CODES:
            raise serializers.ValidationError(f"The currency code {value} is not valid. Please use a valid currency.")

        return value



