import os

from django.core.management.base import BaseCommand

from hindex.users.models import User, Team


class Command(BaseCommand):

    def handle(self, *args, **options):
        team, _ = Team.objects.get_or_create(label="Base Team")
        if not User.objects.filter(username='admin'):
            User.objects.create_superuser(
                username='admin', password=os.getenv('ADMIN_PW', 'admin'), team=team)
