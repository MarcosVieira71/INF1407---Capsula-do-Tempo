from django.test import TestCase
from django.utils import timezone

from datetime import timedelta

from ..models import Capsula, Usuario

class CapsulaTest(TestCase):

    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='teste',
            password='123'
        )

    def test_capsula_fechada(self):
        capsula = Capsula.objects.create(
            usuario=self.user,
            titulo="Teste",
            data_abertura=timezone.now() + timedelta(days=1)
        )
        self.assertFalse(capsula.esta_aberta())

    def test_capsula_aberta(self):
        capsula = Capsula.objects.create(
            usuario=self.user,
            titulo="Teste",
            data_abertura=timezone.now() - timedelta(days=1)
        )
        self.assertTrue(capsula.esta_aberta())