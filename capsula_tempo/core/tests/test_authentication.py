"""
Módulo de testes para o fluxo de autenticação e perfis de usuário.

Este módulo contém testes para as funcionalidades de login, 
logout, registro de novos usuários e atualização de perfil.
"""

from django.test import TestCase
from django.urls import reverse

from ..models import Usuario


class AuthenticationTest(TestCase):
    """Testes automatizados para autenticação e gerenciamento de perfil de usuário."""

    def setUp(self):
        """
        Configura o ambiente inicial para cada teste.
        
        Cria um dicionário de dados de exemplo e um usuário existente no banco
        de dados para testes de autenticação.
        """
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
        """Verifica se a página de login é carregada corretamente via GET."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Login')

    def test_login_success(self):
        """Verifica se um usuário existente consegue fazer login com sucesso."""
        response = self.client.post(reverse('login'), {
            'username': 'existinguser',
            'password': 'oldpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lista'))

    def test_login_failure(self):
        """Garante que credenciais inválidas não permitem o acesso."""
        response = self.client.post(reverse('login'), {
            'username': 'existinguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Login') 

    def test_logout(self):
        """Verifica se o logout encerra a sessão e redireciona para o login."""
        self.client.login(username='existinguser', password='oldpass123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_register_page_get(self):
        """Verifica o carregamento da página de registro."""
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro.html')
        self.assertContains(response, 'Criar conta')

    def test_register_success(self):
        """Valida a criação de um novo usuário no banco de dados após o registro."""
        response = self.client.post(reverse('registro'), self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        # Verifica se o usuário foi criado
        user = Usuario.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.nome, 'Test User')

    def test_register_password_mismatch(self):
        """Verifica se o registro falha quando as senhas não coincidem."""
        data = self.user_data.copy()
        data['password2'] = 'differentpass'
        response = self.client.post(reverse('registro'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro.html')
        # Usuário não deve ser criado
        self.assertFalse(Usuario.objects.filter(username='testuser').exists())

    def test_register_duplicate_username(self):
        """Garante que não seja possível registrar dois usuários com o mesmo nome."""
        data = self.user_data.copy()
        data['username'] = 'existinguser'
        response = self.client.post(reverse('registro'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro.html')

    def test_profile_update_page_get(self):
        """Verifica se a página de edição de perfil está acessível para usuários autenticados."""
        self.client.login(username='existinguser', password='oldpass123')
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'perfil.html')
        self.assertContains(response, 'Editar perfil')

    def test_profile_update_success(self):
        """Verifica se os dados do usuário são atualizados corretamente."""
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
        """Garante que usuários não logados sejam redirecionados ao tentar editar perfil."""
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('perfil')}")
    
    def test_password_change_page_get(self):
        """Verifica se a página de alteração de senha é acessível para usuários logados."""
        self.client.login(username='existinguser', password='oldpass123')
        response = self.client.get(reverse('alterar_senha'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'alterar_senha.html')

    def test_password_change_success(self):
        """Valida a troca de senha quando a senha antiga está correta."""
        self.client.login(username='existinguser', password='oldpass123')
        
        response = self.client.post(reverse('alterar_senha'), {
            'old_password': 'oldpass123',
            'new_password1': 'newsecurepass456',
            'new_password2': 'newsecurepass456'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('perfil'))
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newsecurepass456'))

    def test_password_change_wrong_old_password(self):
        """Garante que a senha não seja alterada se a senha antiga estiver incorreta."""
        self.client.login(username='existinguser', password='oldpass123')
        
        response = self.client.post(reverse('alterar_senha'), {
            'old_password': 'wrong_old_password',
            'new_password1': 'newsecurepass456',
            'new_password2': 'newsecurepass456'
        })
        
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        
        self.assertTrue(self.user.check_password('oldpass123'))

    def test_password_change_unauthenticated(self):
        """Verifica se usuários não logados são impedidos de acessar a troca de senha."""
        response = self.client.get(reverse('alterar_senha'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_home_page_authenticated(self):
        """Verifica se a Home exibe a saudação personalizada para usuários logados."""
        self.client.login(username='existinguser', password='oldpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Olá, Existing User')

    def test_home_page_unauthenticated(self):
        """Verifica se a Home não exibe saudações para visitantes anônimos."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertNotContains(response, 'Olá, Existing User')

    def test_profile_icon_links_to_profile_page(self):
        """Verifica se o link para a página de perfil está presente na lista."""
        self.client.login(username="existinguser", password="oldpass123")
        response = self.client.get(reverse("lista"))
        self.assertContains(response, "/perfil/")
    