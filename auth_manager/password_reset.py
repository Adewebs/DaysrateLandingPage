from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from system_user.models import CustomerInfo
from django.contrib.auth.hashers import make_password
from rest_framework import generics  # Import generics


# Password Reset Request Serializer
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetRequestView(generics.GenericAPIView):
    """Request a password reset by email"""
    serializer_class = PasswordResetRequestSerializer  # Explicitly set the serializer class

    def post(self, request, *args, **kwargs):
        # Validate and process request using the serializer
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomerInfo.objects.get(email=email)
            except CustomerInfo.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            # Generate a token for password reset
            reset_token = get_random_string(length=6, allowed_chars="0123456789")
            user.forget_password_token = reset_token
            user.save()

            # Send the reset token to the user's email
            self.send_reset_email(user)

            return Response({"detail": "Password reset token sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_reset_email(self, user):
        """Send the password reset token to the user's email"""
        subject = 'Password Reset Request'
        message = f"Your password reset token is: {user.forget_password_token}"
        send_mail(subject, message, 'from@example.com', [user.email])


# Password Reset Verify Serializer
class PasswordResetVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)


class PasswordResetVerifyView(generics.GenericAPIView):
    """Verify the reset token for password change"""
    serializer_class = PasswordResetVerifySerializer  # Explicitly set the serializer class

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

            # Verify the token
            if user.forget_password_token == token:
                user.password = make_password(new_password)  # Update password
                user.forget_password_token = ""  # Clear the token
                user.save()
                return Response({"detail": "Password successfully reset."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
