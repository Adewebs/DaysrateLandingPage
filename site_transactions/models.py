from django.db import models
from system_user.models import CustomerInfo
from django.conf import settings
class GeneralTransaction(models.Model):
    PAYMENT_CHOICES = settings.PAYMENT_CHOICES
    CURRENCY_CHOICES = settings.CURRENCY_CHOICES
    buyer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE, related_name='buyer_exchanging', null=True,blank=True)
    merchant = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE, related_name='merchant_exchanging', null=True,blank=True)
    buyer_currency_exchange = models.CharField(max_length=3,choices=CURRENCY_CHOICES,blank=True,null=True)
    merchant_currency_exchange = models.CharField(max_length=3,choices=CURRENCY_CHOICES,blank=True,null=True)
    buyer_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    merchant_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    buyer_previous_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    buyer_new_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    merchant_previous_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    merchant_new_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    buyer_payment_type = models.CharField(max_length=50,choices=PAYMENT_CHOICES,blank=True,null=True)
    is_transaction_successful = models.BooleanField(default=False)
    card_transaction_reference = models.CharField(max_length=255, blank=True, null=True)
    api_transaction_reference = models.CharField(max_length=255, blank=True, null=True)
    transaction_response = models.CharField(max_length=755, blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)


class CardDeposit(models.Model):
    CURRENCY_CHOICES = settings.CURRENCY_CHOICES
    transaction_currency = models.CharField(max_length=3,choices=CURRENCY_CHOICES,blank=True,null=True)
    customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transaction_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    card_transaction_reference = models.CharField(max_length=255, blank=True, null=True)
    api_response = models.CharField(max_length=755, blank=True, null=True)
    is_transaction_successful = models.BooleanField(default=False)
    card_number = models.CharField(max_length=255, blank=True, null=True)
    card_csv = models.CharField(max_length=255, blank=True, null=True)
    card_reccurent_token = models.CharField(max_length=255, blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
