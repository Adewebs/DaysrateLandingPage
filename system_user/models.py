from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomerInfo(AbstractUser):
    COUNTRY_CHOICES = [
        ("NG", "Nigeria"),
        ("GH", "Ghana"),
        ("KE", "Kenya"),
        ("ZA", "South Africa"),
        ("UG", "Uganda"),
        ("US", "USA"),
        ("GB", "UK"),
        ("CA", "Canada"),
        ("AE", "UAE"),
    ]

    CURRENCY_CHOICES = [
        ("NGN", "Nigerian Naira (₦)"),
        ("GHS", "Ghanaian Cedi (₵)"),
        ("KES", "Kenyan Shilling (KSh)"),
        ("ZAR", "South African Rand (R)"),
        ("UGX", "Ugandan Shilling (USh)"),
        ("USD", "US Dollar ($)"),
        ("GBP", "British Pound (£)"),
        ("CAD", "Canadian Dollar (C$)"),
        ("AED", "United Arab Emirates Dirham (د.إ)"),
    ]

    USER_TYPE_CHOICES = [
        ("MERCHANT", "Merchant"),
        ("BUYER", "Buyer"),
    ]

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    country = models.CharField(
        max_length=3,  # 3-character code for country
        choices=COUNTRY_CHOICES,
        blank=True,
        null=True
    )
    user_type = models.CharField(
        max_length=8,  # Merchant or Buyer
        choices=USER_TYPE_CHOICES,
        default="BUYER"  # Default to Buyer
    )

    currency = models.CharField(
        max_length=3,  # Currency code
        choices=CURRENCY_CHOICES,
        blank=True,
        null=True
    )
    user_address = models.CharField(max_length=200, blank=True, null=True)
    transaction_pin = models.CharField(max_length=100, blank=True, null=True)
    is_user_verified = models.BooleanField(default=False)
    is_user_ban = models.BooleanField(default=False)
    is_user_having_update = models.BooleanField(default=False)
    is_transaction_pin_set = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=100, blank=True, null=True,unique=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bvn = models.CharField(max_length=50, blank=True, null=True)
    forget_password_token = models.CharField(max_length=255, blank=True, null=True)
    registration_token = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to='customer_profile_image/', blank=True, null=True)
    verification_document_id = models.CharField(max_length=255, blank=True, null=True)
    user_documents = models.FileField(upload_to='verification_document/', blank=True, null=True)
    user_face_verification_documents = models.FileField(upload_to='user_face_verification_document/', blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='system_user_group',  # Add a unique related_name
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customer_user_permissions',  # Add a unique related_name
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name}"

    class Meta:
        ordering = ['-id']