from django.test import TestCase
from .models import Reservation, Court
from django.contrib.auth import get_user_model
import datetime
from django.utils.timezone import now
User = get_user_model()

class CourtTest(TestCase):
    def setUp(self):
        self.futsal = Court.objects.create(
            name="Central Fútbol Sala", 
            type="football",
            location="Pabellón Polideportivo"
        )
        self.padel = Court.objects.create(
            name="Pádel Dobles", 
            type="padel",
            location="Pabellón Polideportivo (Exterior)"
        )

    def test_check_courts(self):
        futsal = Court.objects.get(name="Central Fútbol Sala")
        padel = Court.objects.get(name="Pádel Dobles")

        self.assertTrue(isinstance(futsal, Court))
        self.assertTrue(isinstance(padel, Court))

    def test_court_str(self):
        self.assertEqual(str(self.futsal), "Central Fútbol Sala (Fútbol)")
        self.assertEqual(str(self.padel), "Pádel Dobles (Pádel)")


class ReservationTest(TestCase):
    def setUp(self):
        self.testUser = User.objects.create(
            name="Test",
            username="test",
        )
        self.testCourt = Court.objects.create(
            name="Pádel Individual",
            type="padel",
            location="Pabellón Polideportivo (Exterior)"
        )
        self.reservation1 = Reservation.objects.create(
            user=self.testUser,
            court=self.testCourt,
            date=now(),
            start_time=datetime.time(10,0),
            end_time=datetime.time(11,0),
            status="pending"
        )

    def test_reservation_data(self):
        self.assertEqual(self.reservation1.user, self.testUser)
        self.assertEqual(self.reservation1.court, self.testCourt)
        self.assertEqual(self.reservation1.start_time, datetime.time(10,0))
        self.assertEqual(self.reservation1.end_time, datetime.time(11,0))
        self.assertEqual(self.reservation1.status, "pending")