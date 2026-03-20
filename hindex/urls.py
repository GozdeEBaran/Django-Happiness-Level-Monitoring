from django.contrib import admin
from django.urls import path, include, reverse_lazy, re_path
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

admin.site.site_header = 'Happiness Index'
admin.site.site_title = 'Hindex Admin'


API_V1 = "api/v1/"

api_urls = [
    # App
    path('', include('hindex.happiness_levels.urls')),
    path('', include('hindex.utils.urls')),

    # Api Doc
    path('schema/',  SpectacularAPIView.as_view(), name='schema'),
    path('swagger/',  SpectacularSwaggerView.as_view(), name='swagger'),
    path('redoc/',  SpectacularRedocView.as_view(), name='redoc'),

    # Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # app
    path(API_V1, include(api_urls)),

    # drf
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('swagger'), permanent=False)),
]
