from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "orif",
                "first_name": "Orif",
                "last_name": "Sarniyozov",
                "email": "sarniyozovorif@gmail.com",
                "password": "qwertyu"
            }
        )

        user = User.objects.get(username="orif")

        self.assertEqual(user.first_name, "Orifr")
        self.assertEqual(user.last_name, "Sarniyozov")
        self.assertEqual(user.email, "sarniyozovorif@gmail.com")
        self.assertNotEqual(user.password, "qwertyu")
        self.assertTrue(user.check_password("qwertyu"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Orif",
                "email": "sarniyozovorif@gmail.com"
            }
        )

        user_count = User.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "orif",
                "first_name": "Orif",
                "last_name": "Sarniyozov",
                "email": "invalid-email",
                "password": "qwertyu"
            }
        )

        user_count = User.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        # 1. create a user
        # 2. try to create another user with that same username
        # 3. check that the second user was not created
        # 4. check that the form contains the error message
        pass
