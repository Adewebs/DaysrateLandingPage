from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from system_user.models import CustomerInfo
from .serializers import EmailPasswordVerificationSerializer


class EmailPasswordVerificationView(generics.GenericAPIView):
    """View to verify email or password reset token"""
    serializer_class = EmailPasswordVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Initialize serializer with the request data
        serializer = self.get_serializer(data=request.data)

        # Validate the serializer
        if serializer.is_valid():
            user = serializer.validated_data['user']
            is_email_verification = serializer.validated_data['is_email_verification']

            # Process email verification
            if is_email_verification:
                user.is_user_verified = True
                user.registration_token = ""  # Clear the registration token after verification
                user.save()
                return Response({"detail": "Email successfully verified."}, status=status.HTTP_200_OK)

            # Process password reset verification
            else:
                user.forget_password_token = ""  # Clear the password reset token after verification
                user.save()
                return Response({"detail": "Password reset token verified."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
