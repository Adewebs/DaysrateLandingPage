from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MerchantReviewViewSet
from .stripe import create_payment_intent


router = DefaultRouter()
router.register(r'add_review', MerchantReviewViewSet,basename='add_review')

# Wire up the API URLs
urlpatterns = [
    path('', include(router.urls)),
    path('create-payment-intent/', create_payment_intent, name="create-payment-intent"),
]
