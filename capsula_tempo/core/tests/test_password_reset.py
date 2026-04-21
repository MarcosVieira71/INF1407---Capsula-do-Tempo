"""
Módulo de testes para o fluxo de recuperação de senha.

Este módulo valida as views de redefinição de senha, garantindo que o formulário
de solicitação, o envio de e-mail simulado e as páginas de confirmação/sucesso
estejam operando corretamente.
"""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from datetime import timedelta

from ..models import Usuario


class PasswordResetTest(TestCase):
    """Testes para o sistema de recuperação de senha do usuário."""

    def setUp(self):
        """Cria um usuário padrão para validar o envio de solicitações de troca de senha."""
        self.user = Usuario.objects.create_user(
            username='teste',
            password='123',
            email='teste@email.com'
        )

    def test_password_reset_form_get(self):
        """Verifica se a página inicial de solicitação de recuperação de senha carrega corretamente."""
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recuperar senha')
        self.assertTemplateUsed(response, 'password_reset_form.html')

    def test_password_reset_form_post_valid_email(self):
        """Valida se o envio do formulário com um e-mail cadastrado redireciona para a página de sucesso."""
        response = self.client.post(reverse('password_reset'), {
            'email': 'teste@email.com'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('password_reset_done'))

    def test_password_reset_form_post_invalid_email(self):
        """Garante que o sistema redireciona para a página de sucesso mesmo com e-mail inexistente por segurança."""
        response = self.client.post(reverse('password_reset'), {
            'email': 'naoexiste@email.com'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('password_reset_done'))

    def test_password_reset_done_get(self):
        """Verifica a exibição da página que informa ao usuário que o e-mail foi enviado."""
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E-mail enviado')
        self.assertTemplateUsed(response, 'password_reset_done.html')

    def test_password_reset_confirm_invalid_token(self):
        """Valida o comportamento da página de troca de senha quando os parâmetros de segurança (UID ou Token) são inválidos."""
        response = self.client.get(reverse('password_reset_confirm', kwargs={
            'uidb64': 'invalid',
            'token': 'invalid'
        }))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'link de redefinição de senha é inválido')
        self.assertTemplateUsed(response, 'password_reset_confirm.html')

    def test_password_reset_complete_get(self):
        """Verifica a exibição da página final de sucesso, após a senha ter sido redefinida."""
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Senha redefinida')
        self.assertTemplateUsed(response, 'password_reset_complete.html')
