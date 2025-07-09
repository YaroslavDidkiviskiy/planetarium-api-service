from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from planetarium.models import ShowTheme, AstronomyShow, PlanetariumDome, ShowSession, Reservation
import os
from django.conf import settings

User = get_user_model()


class ShowThemeViewSetTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@test.com", password="password", is_staff=True
        )
        self.user = User.objects.create_user(
            email="user@test.com", password="password"
        )
        self.theme = ShowTheme.objects.create(name="Cosmology")
        self.url = reverse("planetarium:showtheme-list")

    def test_admin_can_create_theme(self):
        self.client.force_authenticate(self.admin)
        data = {"name": "Astrophysics"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShowTheme.objects.count(), 2)

    def test_user_can_list_themes_but_not_create(self):
        self.client.force_authenticate(self.user)
        # Перевірка чи може звичайний користувач переглядати
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Перевірка чи не може створювати
        data = {"name": "New Theme"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AstronomyShowViewSetTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@test.com", password="password", is_staff=True
        )
        self.user = User.objects.create_user(
            email="user@test.com", password="password"
        )
        self.theme = ShowTheme.objects.create(name="Cosmology")
        self.show = AstronomyShow.objects.create(title="Black Holes", description="About black holes")
        self.show.theme.add(self.theme)
        self.url = reverse("planetarium:astronomyshow-list")

        # Створюємо тестове зображення
        self.test_image_path = os.path.join(settings.BASE_DIR, "test_image.jpg")
        with open(self.test_image_path, "wb") as f:
            f.write(b"fake image data")

    def tearDown(self):
        # Видаляємо тестове зображення після тестів
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)

    def test_filter_by_theme(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, {"theme": "cosmo"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Black Holes")

    def test_create_show_admin_only(self):
        self.client.force_authenticate(self.admin)
        data = {
            "title": "New Show",
            "description": "New description",
            "theme": [self.theme.id]
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Користувач не може створити
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PlanetariumDomeViewSetTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@test.com", password="password", is_staff=True
        )
        self.user = User.objects.create_user(
            email="user@test.com", password="password"
        )
        self.dome = PlanetariumDome.objects.create(
            name="Main Dome", rows=10, seats_in_row=15
        )
        self.url = reverse("planetarium:planetariumdome-list")

    def test_user_can_list_but_not_create(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        data = {
            "name": "New Dome",
            "rows": 12,
            "seats_in_row": 20
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_dome(self):
        self.client.force_authenticate(self.admin)
        data = {
            "name": "New Dome",
            "rows": 12,
            "seats_in_row": 20
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PlanetariumDome.objects.count(), 2)


class ShowSessionViewSetTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@test.com", password="password", is_staff=True
        )
        self.user = User.objects.create_user(
            email="user@test.com", password="password"
        )
        self.show = AstronomyShow.objects.create(
            title="Journey to Mars",
            description="Experience the red planet"
        )
        self.dome = PlanetariumDome.objects.create(
            name="Space Dome", rows=8, seats_in_row=12
        )
        self.session = ShowSession.objects.create(
            astronomy_show=self.show,
            planetarium_dome=self.dome,
            show_time=timezone.now() + timezone.timedelta(days=7)
        )
        self.list_url = reverse("planetarium:showsession-list")

    def test_user_can_list_sessions(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_can_create_session(self):
        self.client.force_authenticate(self.admin)
        data = {
            "astronomy_show": self.show.id,
            "planetarium_dome": self.dome.id,
            "show_time": (timezone.now() + timezone.timedelta(days=14)).isoformat()
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShowSession.objects.count(), 2)

    def test_user_cannot_create_session(self):
        self.client.force_authenticate(self.user)
        data = {
            "astronomy_show": self.show.id,
            "planetarium_dome": self.dome.id,
            "show_time": timezone.now() + timezone.timedelta(days=14)
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReservationViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            email="other@test.com", password="password"
        )
        self.admin = User.objects.create_user(
            email="admin@test.com", password="password", is_staff=True
        )

        self.show = AstronomyShow.objects.create(
            title="Solar System Tour",
            description="Tour through our solar system"
        )
        self.dome = PlanetariumDome.objects.create(
            name="Observatory", rows=5, seats_in_row=10
        )
        self.session = ShowSession.objects.create(
            astronomy_show=self.show,
            planetarium_dome=self.dome,
            show_time=timezone.now() + timezone.timedelta(days=3)
        )

        self.url = reverse("planetarium:reservation-list")
        self.client.force_authenticate(self.user)

    def test_create_reservation(self):
        data = {
            "tickets": [
                {"row": 1, "seat": 1, "show_session": self.session.id},
                {"row": 1, "seat": 2, "show_session": self.session.id},
            ]
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)

        # Перевіряємо, чи створено квитки
        reservation = Reservation.objects.first()
        self.assertEqual(reservation.tickets.count(), 2)
        self.assertEqual(reservation.user, self.user)

    def test_user_sees_only_own_reservations(self):
        # Створюємо резервацію для поточного користувача
        reservation = Reservation.objects.create(user=self.user)

        # Створюємо резервацію для іншого користувача
        self.client.force_authenticate(self.other_user)
        other_reservation = Reservation.objects.create(user=self.other_user)

        # Перевіряємо для першого користувача
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], reservation.id)

        # Перевіряємо для другого користувача
        self.client.force_authenticate(self.other_user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], other_reservation.id)

    def test_unauthenticated_cannot_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        data = {"tickets": []}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
