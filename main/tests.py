from django.test import TestCase
from .models import Mixes

class MixesTestCase(TestCase):
    def setUp(self):
        Mixes.objects.create(name="Test Mix 1", description="Description 1")

    def test_mixes_creation(self):
        mix = Mixes.objects.get(name="Test Mix 1")
        self.assertEqual(mix.description, "Description 1")
