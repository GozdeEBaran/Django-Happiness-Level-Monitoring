from django.conf import settings


def from_settings(request):
    return {
        'ENVIRONMENT_NAME': settings.TIER,
        'ENVIRONMENT_COLOR': settings.ENVIRONMENT_COLOR,
    }
