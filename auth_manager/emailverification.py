from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from system_user.models import CustomerInfo
from .serializers import VerifyRegistrationSerializer
from drf_spectacular.utils import extend_schema


class EmailVerificationView(APIView):
    @extend_schema(
        request=VerifyRegistrationSerializer,
        responses={200: OpenApiResponse(description="User verified successfully."),
                   400: OpenApiResponse(description="Invalid email or registration token.")}
    )
    def post(self, request):
        serializer = VerifyRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomerInfo.objects.get(email=email)
            user.is_user_verified = True
            user.save()

            return Response({"message": "User verified successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
