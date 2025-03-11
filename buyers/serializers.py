from rest_framework import serializers
from merchant.models import MerchantReview, MerchantBuyingRate


class MerchantReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantReview
        fields = '__all__'
        read_only_fields = ['id']

