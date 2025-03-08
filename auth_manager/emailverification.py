from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from system_user.models import CustomerInfo
from rest_framework import serializers
from rest_framework import generics


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()


class EmailVerificationView(generics.GenericAPIView):
    """Verify the registration token from the email verification request"""
    serializer_class = EmailVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Check if the request data is valid
        if not request.data:
            return Response({"detail": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EmailVerificationSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            token = serializer.validated_data['token']

            try:
                user = CustomerInfo.objects.get(email=email)
            except CustomerInfo.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            # Check if the token matches
            if user.registration_token == token:
                user.is_user_verified = True
                user.registration_token = ""  # Clear the token once verified
                user.save()
                return Response({"detail": "Email successfully verified."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        # If the serializer is not valid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

