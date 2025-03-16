from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import GeneralTransaction,CardDeposit
from .serializers import GeneralTransactionSerializer,CardTransactionSerializer



class GeneralTransactionView(viewsets.ModelViewSet):
    serializer_class = GeneralTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view will return the list of Transactions for the currently authenticated user.
        Admin users can see all records.
        """
        user = self.request.user
        if user.is_staff:
            return GeneralTransactionSerializer.objects.all()  # Return all records for admins
        elif user.user_type == "BUYER":
            return GeneralTransactionSerializer.objects.filter(buyer=user)
        elif user.user_type == "MERCHANT":
            return GeneralTransactionSerializer.objects.filter(merchant=user)
        return GeneralTransactionSerializer.objects.all(buyer=user)  # Return only the records of the authenticated user

    def perform_update(self, serializer):
        """
        Ensure that users can only update their own records.
        Admin users can update any record.
        """
        user = self.request.user

        # Check if the user is an admin
        if not user.is_staff:
            # Ensure the user can only update their own record
            if serializer.instance.merchant != user or serializer.instance.buyer != user:
                raise PermissionDenied("You can only update your own record.")

        # Proceed with updating the record
        serializer.save()


class CardTransactionView(viewsets.ModelViewSet):
    serializer_class = CardTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view will return the list of Transactions for the currently authenticated user.
        Admin users can see all records.
        """
        user = self.request.user
        if user.is_staff:
            return CardTransactionSerializer.objects.all()  # Return all records for admins
        return CardTransactionSerializer.objects.all(customer=user)

    def perform_update(self, serializer):
        """
        Ensure that users can only update their own records.
        Admin users can update any record.
        """
        user = self.request.user

        # Check if the user is an admin
        if not user.is_staff:
            # Ensure the user can only update their own record
            if serializer.instance.customer != user:
                raise PermissionDenied("You can only update your own record.")

        # Proceed with updating the record
        serializer.save()
