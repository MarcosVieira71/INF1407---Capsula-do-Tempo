from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from datetime import timedelta

from ..models import Usuario


class PasswordResetTest(TestCase):

    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='teste',
            password='123',
            email='teste@email.com'
        )

    def test_password_reset_form_get(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recuperar senha')
        self.assertTemplateUsed(response, 'password_reset_form.html')

    def test_password_reset_form_post_valid_email(self):
        response = self.client.post(reverse('password_reset'), {
            'email': 'teste@email.com'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('password_reset_done'))

    def test_password_reset_form_post_invalid_email(self):
        response = self.client.post(reverse('password_reset'), {
            'email': 'naoexiste@email.com'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('password_reset_done'))

    def test_password_reset_done_get(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E-mail enviado')
        self.assertTemplateUsed(response, 'password_reset_done.html')

    def test_password_reset_confirm_invalid_token(self):
        response = self.client.get(reverse('password_reset_confirm', kwargs={
            'uidb64': 'invalid',
            'token': 'invalid'
        }))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'link de redefinição de senha é inválido')
        self.assertTemplateUsed(response, 'password_reset_confirm.html')

    def test_password_reset_complete_get(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Senha redefinida')
        self.assertTemplateUsed(response, 'password_reset_complete.html')
