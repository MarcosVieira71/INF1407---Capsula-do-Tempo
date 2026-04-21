"""
Testes unitários para o modelo Capsula.

Este módulo contém testes de validação de campos e lógica interna do modelo,
garantindo que as regras de negócio de datas e estados de abertura sejam respeitadas.
"""

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

from ..models import Capsula, Usuario

class CapsulaTest(TestCase):
    """Testes de integridade e dos métodos da Capsula."""

    def setUp(self):
        """Configura o usuário necessário para a criação das instâncias de Capsula nos testes."""
        self.user = Usuario.objects.create_user(
            username='teste',
            password='123'
        )

    def test_nao_permite_data_no_passado(self):
        """Garante que o método full_clean() lance um erro se a data de abertura estiver no passado."""
        capsula = Capsula(
            usuario=self.user,
            titulo="Teste",
            data_abertura=timezone.localdate() - timedelta(days=1)
        )

        with self.assertRaises(ValidationError):
            capsula.full_clean()

    def test_capsula_fechada(self):
        """Verifica se uma cápsula com data futura é identificada corretamente como fechada."""
        capsula = Capsula.objects.create(
            usuario=self.user,
            titulo="Teste",
            data_abertura=timezone.localdate() + timedelta(days=1)
        )
        self.assertFalse(capsula.esta_aberta())

    def test_capsula_aberta(self):
        """Verifica se uma cápsula com data de abertura igual ou anterior a hoje é identificada como aberta."""
        capsula = Capsula.objects.create(
            usuario=self.user,
            titulo="Teste",
            data_abertura=timezone.localdate() + timedelta(days=1)
        )

        capsula.data_abertura = timezone.localdate() - timedelta(days=1)

        self.assertTrue(capsula.esta_aberta())