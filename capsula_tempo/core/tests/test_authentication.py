from django.test import TestCase
from django.urls import reverse

from ..models import Usuario


class AuthenticationTest(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'nome': 'Test User',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        self.user = Usuario.objects.create_user(
            username='existinguser',
            password='oldpass123',
            email='existing@example.com',
            nome='Existing User'
        )

    def test_login_page_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Login')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'existinguser',
            'password': 'oldpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lista'))

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'existinguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Login') 

    def test_logout(self):
        self.client.login(username='existinguser', password='oldpass123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_register_page_get(self):
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro.html')
        self.assertContains(response, 'Criar conta')

    def test_register_success(self):
        response = self.client.post(reverse('registro'), self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        # Verifica se o usuário foi criado
        user = Usuario.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.nome, 'Test User')

    def test_register_password_mismatch(self):
        data = self.user_data.copy()
        data['password2'] = 'differentpass'
        response = self.client.post(reverse('registro'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro.html')
        # Usuário não deve ser criado
        self.assertFalse(Usuario.objects.filter(username='testuser').exists())

    def test_register_duplicate_username(self):
        data = self.user_data.copy()
        data['username'] = 'existinguser'
        response = self.client.post(reverse('registro'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro.html')

    def test_profile_update_page_get(self):
        self.client.login(username='existinguser', password='oldpass123')
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'perfil.html')
        self.assertContains(response, 'Editar perfil')

    def test_profile_update_success(self):
        self.client.login(username='existinguser', password='oldpass123')
        response = self.client.post(reverse('perfil'), {
            'username': 'existinguser', 
            'nome': 'Updated Name',
            'email': 'updated@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lista'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.nome, 'Updated Name')
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_profile_update_unauthenticated(self):
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('perfil')}")

    def test_home_page_authenticated(self):
        self.client.login(username='existinguser', password='oldpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Olá, Existing User')

    def test_home_page_unauthenticated(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertNotContains(response, 'Olá, Existing User')

    def test_profile_icon_links_to_profile_page(self):
        self.client.login(username="existinguser", password="oldpass123")
        response = self.client.get(reverse("lista"))
        self.assertContains(response, "/perfil/")
    