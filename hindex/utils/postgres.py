import logging

from time import sleep
from django.conf import settings
from django.db import connections, OperationalError


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def wait_for_postgres(recursive=True):
    try:
        if settings.configured:
            connection = connections[list(settings.DATABASES.keys())[0]]
            connection.ensure_connection()
            return True
    except OperationalError:
        logger.info("Postgres isn't ready.")
        if recursive:
            sleep(30)
            return wait_for_postgres()
    return False
