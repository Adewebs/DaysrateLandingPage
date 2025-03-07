from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerInfoViewSet
from .emailverification import EmailVerificationView
from .password_reset import PasswordResetRequestView, PasswordResetVerifyView

router = DefaultRouter()
router.register(r'', CustomerInfoViewSet, basename='customerinfo')

urlpatterns = [
    path('', include(router.urls)),  # This will handle all CRUD operations for customers
    path('verify-email/', EmailVerificationView.as_view(), name='verify-email'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset/verify/', PasswordResetVerifyView.as_view(), name='password-reset-verify'),
]
