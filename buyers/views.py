from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema
from merchant.models import MerchantReview
from .serializers import MerchantReviewSerializer

@extend_schema(
    description="This viewset allows users to create, retrieve, update, and delete merchant reviews. Regular users can only list and interact with their own reviews, while admins can list all reviews and interact with any review. Only admins can delete reviews.",
)
class MerchantReviewViewSet(viewsets.ModelViewSet):
    serializer_class = MerchantReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the reviews for the currently authenticated user,
        unless the user is an admin, in which case all reviews will be returned.
        """
        user = self.request.user
        if user.is_staff:  # If the user is an admin
            return MerchantReview.objects.all()  # Return all reviews
        return MerchantReview.objects.filter(buyer=user)  # Return only reviews by the logged-in user

    def perform_destroy(self, instance):
        """
        Only admins can delete the reviews.
        """
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this review.")
        instance.delete()
