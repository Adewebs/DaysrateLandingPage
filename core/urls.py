from django.contrib import admin
from django.urls import path, include

# To serve static files for production
from django.conf import settings
from django.conf.urls.static import static

# To access API docs - Swagger UI
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
# Core URLs
urlpatterns = [

    # Admin URL
    path("api/v1/admin/", admin.site.urls),
    # Token URLs grouped together
    path('api/v1/token/', include([
        path('obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('verify/', TokenVerifyView.as_view(), name='token_verify'),
        ])),
    # App URLs with a clear header for each app
    # Buyers API URLs
    path('api/v1/buyers/', include('buyers.urls')),
    # Customers API URLs
    path('api/v1/customers/', include('auth_manager.urls')),
    # Merchant API URLs
    path('api/v1/merchant/', include('merchant.urls')),
    # System control configuration URLs
    path('api/v1/config/', include('systemcontrol.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# Add Swagger endpoints if the app is in development mode
if settings.DEBUG:

    urlpatterns += [

        # Schema file endpoint
        path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
        # Optional UI endpoints for documentation
        path('api/v1/documentation/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/v1/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]