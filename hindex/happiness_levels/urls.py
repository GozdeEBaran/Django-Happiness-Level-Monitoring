from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HappinessLevelsViewSet, HappinessStatViewSet

router = DefaultRouter()
router.register(r'happiness-level', HappinessLevelsViewSet, basename="happiness-level")
router.register(r'happiness-stats', HappinessStatViewSet, basename="happiness-stats")

urlpatterns = [
    path('', include(router.urls)),
]
