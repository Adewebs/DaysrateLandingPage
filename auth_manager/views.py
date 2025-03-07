from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from system_user.models import CustomerInfo
from .serializers import CustomerInfoSerializer, CustomerInfoRetrieveSerializer

@extend_schema_view(
    create=extend_schema(
        description="Create a new Buyer account. No authentication required.",
        responses={
            201: CustomerInfoSerializer,
            400: OpenApiResponse(description="Bad request due to validation errors")
        }
    ),
    retrieve=extend_schema(
        description="Retrieve details of the authenticated Customer.",
        responses={
            200: CustomerInfoRetrieveSerializer,  # Return user's details
            401: OpenApiResponse(description="Unauthorized: User must be authenticated")
        }
    ),
    update=extend_schema(
        description="Update the details of the authenticated user. User must be authenticated.",
        responses={
            200: CustomerInfoSerializer,  # Return updated user object
            400: OpenApiResponse(description="Bad request due to validation errors"),
            401: OpenApiResponse(description="Unauthorized: User must be authenticated")
        }
    ),
    partial_update=extend_schema(
        description="Partially update the authenticated user's details.",
        responses={
            200: CustomerInfoSerializer,  # Return partially updated user object
            400: OpenApiResponse(description="Bad request due to validation errors"),
            401: OpenApiResponse(description="Unauthorized: User must be authenticated")
        }
    ),
    destroy=extend_schema(
        description="Delete the authenticated user's account. Only accessible by an admin.",
        responses={
            204: OpenApiResponse(description="Successfully deleted user"),
            401: OpenApiResponse(description="Unauthorized: User must be authenticated"),
            403: OpenApiResponse(description="Forbidden: Only admin can delete user")
        }
    ),
    list=extend_schema(
        description="List all users. Only accessible by an admin.",
        responses={
            200: CustomerInfoRetrieveSerializer(many=True),  # Return a list of user objects
            401: OpenApiResponse(description="Unauthorized: User must be authenticated"),
            403: OpenApiResponse(description="Forbidden: Only admin can list users")
        }
    )
)
class CustomerInfoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CustomerInfo. Handles create, update, get, and delete actions for customers.
    """
    def get_serializer_class(self):
        """
        Return the correct serializer based on the request method.
        """
        if self.action in ['retrieve', 'list']:
            return CustomerInfoRetrieveSerializer
        return CustomerInfoSerializer  # Default to the create/update serializer

    def get_permissions(self):
        """
        Assign permissions based on the action.
        """
        if self.action == 'create':  # POST request - No authentication needed for creating user
            return [AllowAny()]
        elif self.action in ['retrieve', 'update', 'partial_update']:  # GET/PUT/PATCH actions require authentication
            return [IsAuthenticated()]
        elif self.action == 'destroy':  # DELETE requires admin authentication
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action == 'list':  # Admin only for listing users
            return [IsAuthenticated(), IsAdminUser()]

    def get_queryset(self):
        """
        Filter queryset to only return the data of the authenticated user for GET, PUT, PATCH, DELETE actions.
        For admins, return all users when listing.
        """
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return CustomerInfo.objects.filter(id=self.request.user.id)  # Ensure only their own data
        elif self.action == 'list':
            # Only return all users if the requesting user is an admin
            if self.request.user.is_staff:  # is_staff checks if the user is an admin
                return CustomerInfo.objects.all()  # Return all users for admin
            return CustomerInfo.objects.none()  # Return no users if the user is not an admin
        return CustomerInfo.objects.all()  # Return all users for other actions (create for example)
