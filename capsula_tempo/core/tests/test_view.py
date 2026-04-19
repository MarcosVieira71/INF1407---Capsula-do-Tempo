from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from datetime import timedelta

from ..models import Usuario, Capsula, ItemTexto

class ViewTest(TestCase):

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

    def test_capsula_e_finalizada_ao_ser_criada(self):
        self.client.login(username='teste', password='123')

        self.client.post(reverse('criar'), {
            'titulo': 'Minha cápsula',
            'data_abertura': timezone.now() + timedelta(days=1),
            'texto': 'Conteúdo inicial'
        })

        capsula = Capsula.objects.first()
        self.assertTrue(capsula.finalizada)
        