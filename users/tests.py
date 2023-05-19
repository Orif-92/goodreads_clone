from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "orig",
                "first_name": "Orig",
                "last_name": "Carnivorous",
                "email": "sarniyozovorif@gmail.com",
                "password": "qwerty"
            }
        )

        user = CustomUser.objects.get(username="orig")

        self.assertEqual(user.first_name, "Orig")
        self.assertEqual(user.last_name, "Carnivorous")
        self.assertEqual(user.email, "sarniyozovorif@gmail.com")
        self.assertNotEqual(user.password, "qwerty")
        self.assertTrue(user.check_password("qwerty"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Orig",
                "email": "sarniyozovorif@gmail.com"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "orig",
                "first_name": "Orig",
                "last_name": "Carnivorous",
                "email": "invalid-email",
                "password": "qwerty"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        user = CustomUser.objects.create(username="orig", first_name="Orig")
        user.set_password("qwerty")
        user.save()

        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "orig",
                "first_name": "Orig",
                "last_name": "Carnivorous",
                "email": "sarniyozovorif@gmail.com",
                "password": "qwerty"
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, "form", "username", "A user with that username already exists.")

    class LoginTestCase(TestCase):
        def setUp(self):
            # DRY - Don't repeat yourself
            self.db_user = CustomUser.objects.create(username="orig", first_name="Orig")
            self.db_user.set_password("qwerty")
            self.db_user.save()

        def test_successful_login(self):
            self.client.post(
                reverse("users:login"),
                data={
                    "username": "orig",
                    "password": "qwerty"
                }
            )

            user = get_user(self.client)
            self.assertTrue(user.is_authenticated)

        def test_wrong_credentials(self):
            self.client.post(
                reverse("users:login"),
                data={
                    "username": "wrong-username",
                    "password": "qwerty"
                }
            )

            user = get_user(self.client)
            self.assertFalse(user.is_authenticated)

            self.client.post(
                reverse("users:login"),
                data={
                    "username": "orig",
                    "password": "wrong-password"
                }
            )

            user = get_user(self.client)
            self.assertFalse(user.is_authenticated)

        def test_logout(self):
            self.client.login(username="orig", password="qwerty")

            self.client.get(reverse("users:logout"))

            user = get_user(self.client)
            self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username="orig", first_name="Orig", last_name="Carnivorous", email="sarniyozovorif@gmail.com"
        )
        user.set_password("qwerty")
        user.save()

        self.client.login(username="orig", password="qwerty")

        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)
