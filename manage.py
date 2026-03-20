#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import configurations

from dotenv import load_dotenv
load_dotenv()

environment = os.getenv('TIER', "local").title()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'hindex.config.{environment.lower()}')
os.environ.setdefault("DJANGO_CONFIGURATION", environment)

configurations.setup()


def main():
    """Run administrative tasks."""

    if os.getenv('DEBUG_VS_CODE'):
        if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
            import ptvsd

            ptvsd.enable_attach(address=('0.0.0.0', 3000))
            print('Attached!')  # noqa

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
