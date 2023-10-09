from django.test import TestCase
from django.urls import reverse


class GreetingsTests(TestCase):
    def test_home_view(self):
        """
        Function to test home view.
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
