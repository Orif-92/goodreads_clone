from django.contrib.auth import get_user
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

        user = get(username="orif")

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
        user = User.objects.create(username="jakhongir", first_name="Jakhongir")
        user.set_password("somepass")
        user.save()

        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "orif",
                "first_name": "Orif",
                "last_name": "Sarniyozov",
                "email": "sarniyozovorif@gmail.com",
                "password": "qwertyu"
            }
        )

        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, "form", "username", "A user with that username already exists.")

        class LoginTestCase(TestCase):
            def test_successful_login(self):
                db_user = User.objects.create(username="orif", first_name="Orif")
                db_user.set_password("qwertyu")
                db_user.save()

                self.client.post(
                    reverse("users:login"),
                    data={
                        "username": "orif",
                        "password": "qwertyu"
                    }
                )

                user = get_user(self.client)
                self.assertTrue(user.is_authenticated)

            def test_wrong_credentials(self):
                db_user = User.objects.create(username="orif", first_name="Orif")
                db_user.set_password("qwertyu")
                db_user.save()

                self.client.post(
                    reverse("users:login"),
                    data={
                        "username": "wrong-username",
                        "password": "qwertyu"
                    }
                )

                user = get_user(self.client)
                self.assertFalse(user.is_authenticated)

                self.client.post(
                    reverse("users:login"),
                    data={
                        "username": "orif",
                        "password": "wrong-password"
                    }
                )

                user = get_user(self.client)
                self.assertFalse(user.is_authenticated)