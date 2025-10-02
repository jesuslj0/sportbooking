from django.test import TestCase
from .models import Reservation, Court

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
