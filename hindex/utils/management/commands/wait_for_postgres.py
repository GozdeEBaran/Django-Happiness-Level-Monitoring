from django.core.management.base import BaseCommand
from hindex.utils.postgres import wait_for_postgres


class Command(BaseCommand):
    help = 'Wait for the postgres DB to be ready for connections'

    def handle(self, *args, **options):
        wait_for_postgres()
