from django.test import TestCase
from hindex.happiness_levels.validators import validate_level_limit


class HappinessLevelModelTestCase(TestCase):
    def test_level_validator(self):
        with self.assertRaisesMessage(Exception, "Please enter the level 1-10"):
            validate_level_limit(15)

        # it should be good otherwise
        validate_level_limit(5)
