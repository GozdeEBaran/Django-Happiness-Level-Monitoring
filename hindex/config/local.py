import os
from .common import Common
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True
    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS + [
        'debug_toolbar',
        'django_extensions',
    ]

    MIDDLEWARE = Common.MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
