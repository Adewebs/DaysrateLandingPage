from rest_framework import serializers
from .models import MerchantBuyingRate


class MerchantBuyingRateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MerchantBuyingRate
        fields = '__all__'
        read_only_fields = ['id']
