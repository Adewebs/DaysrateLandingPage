from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListSystemMerchant


router = DefaultRouter()
router.register(r'all_merchant', ListSystemMerchant,basename='all_merchant')

# Wire up the API URLs
urlpatterns = [
    path('', include(router.urls)),
]
