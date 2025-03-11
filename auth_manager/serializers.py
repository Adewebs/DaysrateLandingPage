from rest_framework import serializers
from system_user.models import CustomerInfo
from django.contrib.auth.password_validation import validate_password



class VerifyRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    registration_token = serializers.CharField(max_length=255)

    def validate(self, attrs):
        """
        Custom validation to ensure the registration token matches the one stored in the user's record.
        """
        email = attrs.get('email')
        registration_token = attrs.get('registration_token')

        try:
            # Get the user based on the email
            user = CustomerInfo.objects.get(email=email)
        except CustomerInfo.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        # Check if the registration token matches the one stored for this user
        if user.registration_token != registration_token:
            raise serializers.ValidationError("Invalid registration token.")

        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate that the email exists in the system.
        """
        try:
            user = CustomerInfo.objects.get(email=value)
        except CustomerInfo.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class PasswordResetVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate_new_password(self, value):
        """
        Validate the password using Django's password validators.
        """
        try:
            validate_password(value)
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return value



