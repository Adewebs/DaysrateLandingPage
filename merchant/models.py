from django.db import models
from system_user.models import CustomerInfo
from site_transactions.models import GeneralTransaction
from django.conf import settings
class MerchantReview(models.Model):
    merchant = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE, related_name='reviewed_merchant')
    buyer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE,related_name='reviewing_buyer')
    buyer_feedback = models.CharField(max_length=755, blank=True, null=True)
    buyer_rating = models.IntegerField(default=0)
    transaction = models.ForeignKey(GeneralTransaction, on_delete=models.CASCADE)
    review_rating = models.IntegerField(default=0)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer_feedback} {self.buyer} {self.review_rating} {self.review_date}"

    class Meta:
        ordering = ['-review_date']

class MerchantBuyingRate(models.Model):
    CURRENCY_CHOICES = settings.CURRENCY_CHOICES
    merchant = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3,choices=CURRENCY_CHOICES,blank=True,null=True)
    buying_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now_add=True)