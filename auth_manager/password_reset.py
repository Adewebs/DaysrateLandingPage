from datetime import timezone

from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from system_user.models import CustomerInfo
from .serializers import PasswordResetRequestSerializer, PasswordResetVerifySerializer


class PasswordResetRequestView(generics.GenericAPIView):
    """Request a password reset by email."""
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        # Validate and process request using the serializer
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomerInfo.objects.get(email=email)
            except CustomerInfo.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            # Generate a token for password reset and set expiration
            reset_token = user.generate_reset_token()

            # Send the reset token to the user's email
            self.send_reset_email(user)

            return Response({"detail": "Password reset token sent."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_reset_email(self, user):
        """Send the password reset token to the user's email."""
        subject = 'Password Reset Request'
        message = f"Your password reset token is: {user.forget_password_token}\n\nThe token expires in 15 minutes."
        send_mail(subject, message, 'from@example.com', [user.email])


class PasswordResetVerifyView(generics.GenericAPIView):
    """Verify the reset token for password change."""
    serializer_class = PasswordResetVerifySerializer

    def post(self, request, *args, **kwargs):
        # Validate and process request using the serializer
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']

            try:
                user = CustomerInfo.objects.get(email=email)
            except CustomerInfo.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            # Check if the token is valid and not expired
            if user.forget_password_token != token:
                return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the token is expired
            if user.token_expiration < timezone.now():
                return Response({"detail": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)

            # Update password and clear the reset token
            user.password = make_password(new_password)
            user.forget_password_token = ""  # Clear the token
            user.token_expiration = None  # Clear the expiration time
            user.save()

            return Response({"detail": "Password successfully reset."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
