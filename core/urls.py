from django.contrib import admin
from django.urls import path, include

# to serve static file for production
from django.conf import settings
from django.conf.urls.static import static

# to access api docs - swagger ui
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
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path("api/v1/admin/", admin.site.urls),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/buyers/', include('buyers.urls')),
    path('api/v1/merchant/', include('merchant.urls')),
    path('api/v1/config/', include('systemcontrol.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# added to serve static files for development

# Add Swagger endpoint if the app is in development mode
if settings.DEBUG:
    urlpatterns += [
        # Schema file endpoint
        path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
        # Optional UI endpoints
        path('api/v1/documentation/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/v1/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    ]
