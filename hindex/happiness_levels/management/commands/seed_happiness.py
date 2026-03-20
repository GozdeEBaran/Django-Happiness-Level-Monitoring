import csv
import os
import random

from django.core.management.base import BaseCommand
from django.db import transaction

from hindex.config import BASE_DIR
from hindex.users.models import User, Team
from hindex.happiness_levels.models import HappinessLevel


class Command(BaseCommand):
    help = 'Seed all Lines of Business'

    @transaction.atomic
    def handle(self, *args, **options):
        # Faster then get_or_create
        happiness_map = {f"{h.user_id}{h.created_at}": h for h in HappinessLevel.objects.all()}

        with open(os.path.join(BASE_DIR, 'fixtures/SeedHappiness.csv'), 'r') as _file:
            reader = csv.DictReader(_file)
            happiness_bulk = []
            for row in reader:
                # Something is wrong with the header first value
                # it is supposed to be level but reads as below;
                # TODO: Fix it
                level = '\ufefflevel'

                team, _ = Team.objects.get_or_create(label=row.get("team"), province=row.get("province"))
                user, _ = User.objects.get_or_create(username=row.get(
                    "user"), password=row.get('password'), team=team)

                h = happiness_map.get(f"{user.id}{row.get('date')}")
                if not h:
                    happiness_bulk.append(HappinessLevel(
                        level=row.get(level),
                        created_at=row.get('date'),
                        user=user,
                        factor=random.choice(HappinessLevel.HappinessLevelFactor.choices)[0]
                    ))
            HappinessLevel.objects.bulk_create(happiness_bulk)
