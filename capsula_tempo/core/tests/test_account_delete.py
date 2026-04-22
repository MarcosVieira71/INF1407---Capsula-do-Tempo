from django.test import TestCase
from django.urls import reverse

from ..models import Usuario


class AccountDeleteTest(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='todelete',
            password='pass12345',
            email='del@example.com',
            nome='To Delete'
        )

    def test_confirm_page_requires_login(self):
        response = self.client.get(reverse('perfil_excluir'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_confirm_page_shows_for_logged_in(self):
        self.client.login(username='todelete', password='pass12345')
        response = self.client.get(reverse('perfil_excluir'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'perfil_excluir_confirm.html')
        self.assertContains(response, 'Confirmar exclusão da conta')

    def test_post_deletes_user_and_redirects(self):
        self.client.login(username='todelete', password='pass12345')
        response = self.client.post(reverse('perfil_excluir'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        self.assertFalse(Usuario.objects.filter(username='todelete').exists())

    def test_post_requires_login(self):
        response = self.client.post(reverse('perfil_excluir'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)
