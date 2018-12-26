from django.test import TestCase

from ..models import User


class UserTestCase(TestCase):
    def test_str(self):
        user = User(username="demo")
        self.assertEqual(str(user), "demo")
