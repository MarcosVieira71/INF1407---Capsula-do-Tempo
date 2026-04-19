from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from datetime import timedelta

from ..models import Usuario, Capsula, ItemTexto

class CapsulaViewTest(TestCase):

    def setUp(self):
        self.user = Usuario.objects.create_user(username='teste', password='123', email="teste@email.com")

    def test_criar_capsula_logado(self):
        self.client.login(username='teste', password='123')

        response = self.client.post(reverse('criar'), {
            'titulo': 'Minha cápsula',
            'data_abertura': timezone.now() + timedelta(days=1),
            'texto': 'Conteúdo inicial'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Capsula.objects.count(), 1)

    def test_nao_cria_capsula_sem_conteudo(self):
        self.client.login(username='teste', password='123')

        response = self.client.post(reverse('criar'), {
            'titulo': 'Minha cápsula',
            'data_abertura': timezone.now() + timedelta(days=1)
        })

        self.assertEqual(response.status_code, 200) 
        self.assertEqual(Capsula.objects.count(), 0)

    def test_post_capsula_nao_logado(self):
        response = self.client.post(reverse('criar'), {
            'titulo': 'Teste',
            'data_abertura': timezone.now() + timedelta(days=1)
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Capsula.objects.count(), 0)

    def test_capsula_associada_ao_usuario(self):
        self.client.login(username='teste', password='123')

        self.client.post(reverse('criar'), {
            'titulo': 'Teste',
            'data_abertura': timezone.now() + timedelta(days=1),
            'texto': 'Conteúdo'
        })

        capsula = Capsula.objects.first()

        self.assertEqual(capsula.usuario, self.user)

    def test_abrir_capsula_antes_data_abertura(self):
        capsula = Capsula.objects.create(
            usuario=self.user,
            titulo='Teste',
            data_abertura=timezone.now() + timedelta(days=1)
        )

        self.client.login(username='teste', password='123')
        response = self.client.get(reverse('detalhe', args=[capsula.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A cápsula só pode ser aberta')

    def test_abrir_capsula_apos_data_abertura(self):
        capsula = Capsula.objects.create(
            usuario=self.user,
            titulo='Teste',
            data_abertura=timezone.now() + timedelta(days=1)
        )

        #simula passagem do tempo aqui atualizando dentro do banco
        Capsula.objects.filter(pk=capsula.pk).update(
            data_abertura=timezone.now() - timedelta(days=1)
        )

        ItemTexto.objects.create(capsula=capsula, texto='Mensagem aberta')

        self.client.login(username='teste', password='123')
        response = self.client.get(reverse('detalhe', args=[capsula.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mensagem aberta')

    def test_capsula_nao_pode_ser_editada(self):
        capsula = Capsula.objects.create(
            usuario=self.user,
            titulo='Original',
            data_abertura=timezone.now() + timedelta(days=1)
        )

        capsula.titulo = 'Alterado'
        with self.assertRaises(ValueError):
            capsula.save()

    def test_lista_capsulas_logado(self):
        self.client.login(username='teste', password='123')
        response = self.client.get(reverse('lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lista de cápsulas")

    def test_lista_filtrada_por_usuario(self):
        user2 = Usuario.objects.create_user(username='outro', password='123', email="outro@email.com")

        Capsula.objects.create(usuario=self.user, titulo="Minha", data_abertura=timezone.now() + timedelta(days=1))
        Capsula.objects.create(usuario=user2, titulo="Outro", data_abertura=timezone.now() + timedelta(days=1))

        self.client.login(username='teste', password='123')
        response = self.client.get(reverse('lista'))

        self.assertContains(response, "Minha")
        self.assertNotContains(response, "Outro")

    def test_deletar_capsula(self):
        capsula = Capsula.objects.create(
            usuario=self.user,
            titulo="Teste",
            data_abertura=timezone.now() + timedelta(days=1)
        )

        self.client.login(username='teste', password='123')
        response = self.client.post(f'/deletar/{capsula.id}/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Capsula.objects.count(), 0)
    
    def test_nao_deleta_capsula_de_outro_usuario(self):
        user2 = Usuario.objects.create_user(
            username='outro',
            password='123',
            email='outro@email.com'
        )

        capsula = Capsula.objects.create(
            usuario=user2,
            titulo="Privado",
            data_abertura=timezone.now() + timedelta(days=1)
        )

        self.client.login(username='teste', password='123')
        response = self.client.post(f'/deletar/{capsula.id}/')

        self.assertNotEqual(response.status_code, 200)


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
        self.assertContains(response, 'Você está logado')

    def test_home_page_unauthenticated(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Você não está logado')
        