from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import MerchantBuyingRate
from .serializers import MerchantBuyingRateSerializer


@extend_schema_view(
    list=extend_schema(
        description="List all merchant buying rates for the authenticated user. Admin users can see all records."
    ),
    retrieve=extend_schema(
        description="Retrieve a specific merchant buying rate record. Admin users can retrieve any record."
    ),
    update=extend_schema(
        description="Update a specific merchant buying rate record. Users can update only their own record. Admin users can update any record."
    ),
    create=extend_schema(
        description="Create a new merchant buying rate record. Admins can create records for any merchant."
    )
)
class MerchantBuyingRateViewSet(viewsets.ModelViewSet):
    serializer_class = MerchantBuyingRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view will return the list of buying rates for the currently authenticated user.
        Admin users can see all records.
        """
        user = self.request.user
        if user.is_staff:
            return MerchantBuyingRate.objects.all()  # Return all records for admins
        return MerchantBuyingRate.objects.filter(merchant=user)  # Return only the records of the authenticated user

    def perform_update(self, serializer):
        """
        Ensure that users can only update their own records.
        Admin users can update any record.
        """
        user = self.request.user

        # Check if the user is an admin
        if not user.is_staff:
            # Ensure the user can only update their own record
            if serializer.instance.merchant != user:
                raise PermissionDenied("You can only update your own record.")

        # Proceed with updating the record
        serializer.save()
