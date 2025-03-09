from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerInfoViewSet


router = DefaultRouter()
router.register(r'', CustomerInfoViewSet, basename='customerinfo')

urlpatterns = [
    path('', include(router.urls)),
]
