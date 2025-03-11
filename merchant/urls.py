from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MerchantBuyingRateViewSet


router = DefaultRouter()
router.register(r'update_buying_rate', MerchantBuyingRateViewSet,basename='update_buying_rate')

# Wire up the API URLs
urlpatterns = [
    path('', include(router.urls)),
]
