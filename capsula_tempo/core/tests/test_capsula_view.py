"""
Testes de interface e lógica de negócio para o gerenciamento de Cápsulas.

Este módulo valida o ciclo de vida das cápsulas do tempo, incluindo criação, 
listagem filtrada, restrições de abertura por data e edição protegida por senha.
"""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from datetime import timedelta

from ..models import Usuario, Capsula, ItemTexto


class CapsulaViewTest(TestCase):
    """Conjunto de testes para as views relacionadas às Cápsulas."""

    def setUp(self):
        """Prepara o ambiente de teste com um usuário padrão."""
        self.user = Usuario.objects.create_user(username='teste', password='123', email="teste@email.com")

    def test_create_capsule_logged_in(self):
        """Verifica se um usuário logado consegue criar uma cápsula com sucesso."""
        self.client.login(username='teste', password='123')

        response = self.client.post(reverse('criar'), {
            'titulo': 'Minha cápsula',
            'data_abertura': timezone.localdate() + timedelta(days=1),
            'texto': 'Conteúdo inicial',
            'senha': 'segredo123'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Capsula.objects.count(), 1)

    def test_does_not_create_capsule_without_content(self):
        """Garante que uma cápsula não seja criada se faltarem campos obrigatórios."""
        self.client.login(username='teste', password='123')

        response = self.client.post(reverse('criar'), {
            'titulo': 'Minha cápsula',
            'data_abertura': timezone.localdate()+ timedelta(days=1)
        })

        self.assertEqual(response.status_code, 200) 
        self.assertEqual(Capsula.objects.count(), 0)

    def test_post_capsule_not_logged_in(self):
        """Verifica se usuários anônimos são impedidos de criar novas cápsulas."""
        response = self.client.post(reverse('criar'), {
            'titulo': 'Teste',
            'data_abertura': timezone.localdate()+ timedelta(days=1)
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Capsula.objects.count(), 0)

    def test_capsule_associated_with_user(self):
        """Confirma se a cápsula recém-criada é vinculada corretamente ao autor."""
        self.client.login(username='teste', password='123')

        self.client.post(reverse('criar'), {
            'titulo': 'Teste',
            'data_abertura': timezone.localdate()+ timedelta(days=1),
            'texto': 'Conteúdo',
            'senha': 'segredo123'
        })

        capsula = Capsula.objects.first()

        self.assertEqual(capsula.usuario, self.user)

    def test_open_capsule_before_opening_date(self):
        """Garante que o conteúdo da cápsula permaneça oculto antes da data de abertura."""
        capsula = Capsula.objects.create(
            usuario=self.user,
            titulo='capsula-teste',
            data_abertura=timezone.localdate() + timedelta(days=7)
        )

        ItemTexto.objects.create(capsula=capsula, texto='conteudo-teste')

        self.client.login(username='teste', password='123')
        response = self.client.get(reverse('detalhe', args=[capsula.pk]))

        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, 'Esta cápsula ainda está selada')
        self.assertContains(response, capsula.data_abertura.strftime('%d/%m/%Y'))
        
        self.assertNotContains(response, 'conteudo-teste')

    def test_open_capsule_after_opening_date(self):
        """Verifica se o conteúdo é liberado para visualização após atingir a data de abertura."""
        capsula = Capsula.objects.create(
            usuario=self.user,
            titulo='capsula-teste',
            data_abertura=timezone.localdate() + timedelta(days=1)
        )
        ItemTexto.objects.create(capsula=capsula, texto='conteudo-teste')

        Capsula.objects.filter(pk=capsula.pk).update(
            data_abertura=timezone.localdate() - timedelta(days=1)
        )

        self.client.login(username='teste', password='123')
        response = self.client.get(reverse('detalhe', args=[capsula.pk]))

        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, 'conteudo-teste') 
        
        self.assertNotContains(response, 'Esta cápsula ainda está selada')


    def test_list_capsules_logged_in(self):
        """Valida se a página de listagem carrega corretamente para usuários autenticados."""
        self.client.login(username='teste', password='123')
        response = self.client.get(reverse('lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Minhas Cápsulas")

    def test_list_filtered_by_user(self):
        """Garante que um usuário veja apenas as suas próprias cápsulas e não as de terceiros."""
        user2 = Usuario.objects.create_user(username='outro', password='123', email="outro@email.com")

        Capsula.objects.create(usuario=self.user, titulo="Minha", data_abertura=timezone.localdate()+ timedelta(days=1))
        Capsula.objects.create(usuario=user2, titulo="Outro", data_abertura=timezone.localdate()+ timedelta(days=1))

        self.client.login(username='teste', password='123')
        response = self.client.get(reverse('lista'))

        self.assertContains(response, "Minha")
        self.assertNotContains(response, "Outro")

    def test_delete_capsule(self):
        """Verifica se o proprietário consegue excluir sua cápsula."""
        capsula = Capsula.objects.create(
            usuario=self.user,
            titulo="Teste",
            data_abertura=timezone.localdate()+ timedelta(days=1)
        )

        self.client.login(username='teste', password='123')
        response = self.client.post(f'/deletar/{capsula.id}/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Capsula.objects.count(), 0)
    
    def test_does_not_delete_other_users_capsule(self):
        """Impede que um usuário exclua uma cápsula que não lhe pertence."""
        user2 = Usuario.objects.create_user(
            username='outro',
            password='123',
            email='outro@email.com'
        )

        capsula = Capsula.objects.create(
            usuario=user2,
            titulo="Privado",
            data_abertura=timezone.localdate()+ timedelta(days=1)
        )

        self.client.login(username='teste', password='123')
        response = self.client.post(f'/deletar/{capsula.id}/')

        self.assertNotEqual(response.status_code, 200)

    def test_editing_without_auth(self):
        """Garante que a edição seja bloqueada se a permissão de edição não estiver na sessão."""
        self.client.login(username='teste', password='123')

        self.client.post(reverse('criar'), {
            'titulo': 'EditTest',
            'data_abertura': timezone.localdate()+ timedelta(days=1),
            'texto': 'Original',
            'senha': 'mypass'
        })

        capsula = Capsula.objects.first()
        item = capsula.textos.first()

        response = self.client.post(reverse('editar_itemtexto', args=[item.pk]), {
            'titulo': 'Novo Titulo',
            'data_abertura': timezone.localdate()+ timedelta(days=2),
            'texto': 'Novo Texto'
        })

        self.assertEqual(response.status_code, 302)

        item.refresh_from_db()
        capsula.refresh_from_db()

        self.assertEqual(item.texto, 'Original')
        self.assertEqual(capsula.titulo, 'EditTest')

    def test_auth_edition_with_wrong_password(self):
        """Valida o redirecionamento e erro ao tentar autorizar edição com senha incorreta."""
        self.client.login(username='teste', password='123')

        self.client.post(reverse('criar'), {
            'titulo': 'EditTest',
            'data_abertura': timezone.localdate()+ timedelta(days=1),
            'texto': 'Original',
            'senha': 'mypass'
        })

        capsula = Capsula.objects.first()

        response = self.client.post(reverse('autorizar_edicao', args=[capsula.pk]), {
            'senha': 'wrong'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('lista') + f'?edit={capsula.pk}&wrong=1'
        )

    def test_editing_with_correct_password(self):
        """Verifica o fluxo completo de edição após a autorização bem-sucedida por senha."""
        self.client.login(username='teste', password='123')

        abertura_original = timezone.localdate()+ timedelta(days=1)

        self.client.post(reverse('criar'), {
            'titulo': 'EditTest',
            'data_abertura': abertura_original,
            'texto': 'Original',
            'senha': 'mypass'
        })

        capsula = Capsula.objects.first()
        item = capsula.textos.first()

        response = self.client.post(reverse('autorizar_edicao', args=[capsula.pk]), {
            'senha': 'mypass'
        })

        self.assertEqual(response.status_code, 302)

        session = self.client.session
        session[f'capsula_edit_{capsula.pk}'] = True
        session.save()
        
        nova_data = timezone.localdate()+ timedelta(days=5)

        response = self.client.post(reverse('editar_itemtexto', args=[item.pk]), {
            'titulo': 'Titulo Editado',
            'data_abertura': nova_data,
            'texto': 'Texto Editado'
        })

        self.assertEqual(response.status_code, 302)

        item.refresh_from_db()
        capsula.refresh_from_db()

        self.assertEqual(item.texto, 'Texto Editado')
        self.assertEqual(capsula.titulo, 'Titulo Editado')

    def test_password_cannot_be_changed(self):
        """Garante a integridade da senha, impedindo alterações diretas no campo após a criação."""
        capsula = Capsula.objects.create(
            usuario=self.user,
            titulo='SenhaTest',
            data_abertura=timezone.localdate()+ timedelta(days=1)
        )

        capsula.set_senha('orig')
        capsula.save()

        capsula.refresh_from_db()
        original_hash = capsula.senha

        capsula.senha = 'tampered'
        capsula.save()
        capsula.refresh_from_db()

        self.assertEqual(capsula.senha, original_hash)
        self.assertTrue(capsula.check_senha('orig'))
        self.assertFalse(capsula.check_senha('tampered'))
