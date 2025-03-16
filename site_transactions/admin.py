from django.contrib import admin
from .models import GeneralTransaction,CardDeposit
# Register your models here.

admin.site.register(CardDeposit)
admin.site.register(GeneralTransaction)