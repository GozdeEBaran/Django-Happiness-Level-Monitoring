from django.test.testcases import TestCase
from django.urls import reverse

from hindex.test_runner import APIClient
from hindex.users.test.factories import UserFactory


class EnumsViewsetTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=UserFactory())
        self.url = reverse('enums')

    def test_get_enums(self):
        response = self.client.get(self.url)
        self.assertNotEquals(response.data.get('happinessLevelFactor'), None)
