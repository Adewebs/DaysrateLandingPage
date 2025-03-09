from rest_framework import serializers
from system_user.models import CustomerInfo
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.password_validation import validate_password

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


class CustomerInfoRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInfo
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'country', 'user_type','currency','user_address']


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



