from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MerchantReviewViewSet


router = DefaultRouter()
router.register(r'add_review', MerchantReviewViewSet,basename='add_review')

# Wire up the API URLs
urlpatterns = [
    path('', include(router.urls)),
]
