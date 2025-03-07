from rest_framework import serializers
from system_user.models import CustomerInfo
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

class CustomerInfoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomerInfo
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'country', 'user_type', 'password']  # Specify fields you need

    def validate_email(self, value):
        """Check if the email already exists in the database."""
        if CustomerInfo.objects.filter(email=value).exists():
            raise ValidationError("Email is already taken.")
        return value

    def validate_phone_number(self, value):
        """Check if the phone number already exists in the database."""
        if CustomerInfo.objects.filter(phone_number=value).exists():
            raise ValidationError("Phone number is already taken.")
        return value

    def create(self, validated_data):
        """Override create method to hash the password before saving and ensure it returns the created user."""
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        email = validated_data.get('email')
        validated_data['username'] = email  # Set email as username

        # Create the user and save to the database
        user = CustomerInfo.objects.create(**validated_data)

        # Generate a 6-character token for email verification
        registration_token = get_random_string(length=6, allowed_chars="0123456789")
        user.registration_token = registration_token
        user.save()

        # Send registration email with the verification token
        self.send_registration_email(user)

        return user

    def send_registration_email(self, user):
        """Send a registration email to the user with the registration token."""
        subject = 'Welcome to our service. Please verify your email.'
        message = f"Your email verification token is: {user.registration_token}"
        send_mail(subject, message, 'from@example.com', [user.email])

    def update(self, instance, validated_data):
        """Override update method to hash the password if provided."""
        password = validated_data.get('password', None)
        if password:
            validated_data['password'] = make_password(password)  # Hash the password if updating

        return super().update(instance, validated_data)


# New Serializer for GET requests (Read Only)
class CustomerInfoRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInfo
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'country', 'user_type','currency','user_address']
