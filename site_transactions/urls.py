from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeneralTransactionView,CardTransactionView


router = DefaultRouter()
router.register(r'transaction_history', GeneralTransactionView,basename='transaction_history')
router.register(r'card_transaction_history',CardTransactionView,basename='card_transaction_history')

# Wire up the API URLs
urlpatterns = [
    path('', include(router.urls)),
]
