# Projeto Cápsula do Tempo

Este projeto é uma aplicação web desenvolvida para a disciplina de Programação para a Web na PUC-Rio. A plataforma permite que utilizadores criem "cápsulas digitais" com mensagens e conteúdos que só poderão ser abertos em datas futuras específicas.

## Grupo
* **Julia Gomes Zibordi** 
* **Marcos Paulo Marinho Vieira**

---

## Escopo do projeto
A **Cápsula do Tempo** foi concebida como uma ferramenta de preservação de memórias digitais. O foco principal do desenvolvimento foi criar uma interface autêntica, simulando o envio de envelopes físicos.

**O que foi desenvolvido:**
- Sistema de gestão de cápsulas e de usuários (CRUD completo).
- Recuperação de senha através do envio de e-mails via terminal.
- Controle de acesso por usuário.
- Interface personalizada com animações CSS.
- Testes unitários.
- Deploy do site.

Tudo o que foi desenvolvido está funcionando.

---

## Instruções de uso

### 1. Acesso via site 
Para testar a aplicação diretamente no navegador, acesse o link:
👉 **(https://capsuladotempo.onrender.com/)**

### 2. Execução em ambiente local
Caso deseje rodar o projeto em sua máquina, certifique-se de que tem o Python instalado e siga os passos a seguir.

Você deve configurar o arquivo .env na raiz do projeto. Abaixo está um exemplo:

```bash
SECRET_KEY=teste
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
```

```bash
# 1. Clonar o repositório
git clone https://github.com/MarcosVieira71/INF1407---Capsula-do-Tempo.git

# 2. Instalar dependências necessárias
pip install -r requirements.txt

# 3. Aplicar as migrações do banco de dados
python manage.py migrate

# 4. Iniciar o servidor local
python manage.py runserver

````
---

## Guia de Funcionalidades (Passo a Passo)

### 1. Primeiro acesso e registro
Ao acessar o site, há uma página inicial com as opções "Cápsulas", "Criar cápsula", "Login", "Registrar" e "Esqueci senha". Além disso, há uma breve explicação sobre o conceito das cápsulas do tempo. Para criar o seu usuário, escolha a opção "Registrar".

<div align="center">
<img src="https://github.com/user-attachments/assets/0ba0552a-1e8a-407a-8de8-fba8e6939627" width="700px" />
</div>

Preencha todos os campos do formulário e clique em "Cadastrar".

<div align="center">
<img src="https://github.com/user-attachments/assets/0925034e-2cde-4294-b62a-671b822abb39" width="700px" />
</div>

Se os campos tiverem sido preenchidos corretamente, você será direcionado à página de login. Caso contrário, corrija os campos que estiverem indicados com erro no formulário. 

### 2. Login

A opção de login pode ser acessada através da página inicial clicando em "Login".

<div align="center">
<img src="https://github.com/user-attachments/assets/dc6aa41a-1196-4869-a2e5-844257bdee95" width="700px" />
</div>

Preencha o formulário com o username e a senha que você criou ao se registrar no site. Caso tenha esquecido a sua senha, veja a seção 6 (Recuperação de senha).

<div align="center">
<img src="https://github.com/user-attachments/assets/8efe8a51-1f1a-4c13-80c9-a3aa6e1c21bc" width="700px" />
</div>

### 3. Edição do perfil
Para editar seu perfil, clique em "Olá, [seu username] ou na imagem da moldura no topo direito do site.

<div align="center">
<img src="https://github.com/user-attachments/assets/8896411e-c461-42f5-ad88-709a3375bda1" width="700px" />
</div>

Altere as informações que desejar por meio do formulário e clique em "Salvar" ou clique em "Alterar senha" caso deseje trocar a sua senha.

<div align="center">
<img alt="image" src="https://github.com/user-attachments/assets/f35754c1-036c-4904-ab44-91e8a707de3f"  width="400px" />

</div>

Para alterar a sua senha, insira a senha antiga e confirme a nova. 

<div align="center">
<img src="https://github.com/user-attachments/assets/40f88264-18f7-4465-a8f7-9507ffcab616" width="400px" />
</div>

### 4. Criação de cápsulas do tempo
Para criar uma cápsula do tempo, você precisa estar logado. Para mais informações sobre registro e login, veja as seções 1 (Primeiro acesso e registro) e 2 (Login). Quando estiver pronto, clique em "Criar cápsula".

<div align="center">
<img src="https://github.com/user-attachments/assets/5e7a025d-def9-4e6f-b4ee-657bf27a01ab" width="700px" />
</div>

Preencha a sua cápsula com título, data de abertura e um texto para o seu futuro eu. Além disso, crie uma senha para a sua cápsula. Caso deseje editá-la, será necessário inserir essa senha. 

<div align="center">
<img src="https://github.com/user-attachments/assets/6f04a38d-648f-4fc2-a3f9-cd338d07f8d3" width="450px" />
</div>

Assim que você criar uma cápsula, ela ficará salva no seu perfil. Para ver todas as suas cápsulas criadas, basta clicar em "Cápsulas". 

<div align="center">
<img src="https://github.com/user-attachments/assets/b2276c0c-63d6-4d2f-bc9b-54a2080c54de" width="700px" />
</div>

### 5. Edição de cápsulas do tempo
Para editar uma cápsula do tempo, clique em "Editar". É necessário inserir a senha que você definiu no momento da criação. 

<div align="center">
<img src="https://github.com/user-attachments/assets/04728ae3-e46a-40c3-a479-54f67e2d9832" width="350px" />
</div>

<div align="center">
<img src="https://github.com/user-attachments/assets/7e51a6e6-79d5-4774-9973-2f8c0aabbb97" width="350px" />
</div>

<div align="center">
<img src="https://github.com/user-attachments/assets/146d9efe-b103-49ad-92d4-9fa163f56761" width="350px" />
</div>

Quando estiver satisfeito com as suas mudanças, clique em "Salvar".

⚠️ Não é possível editar cápsulas após a sua data de abertura.

### 6. Recuperação de senha
A recuperação de senha ocorre através do envio de um e-mail pelo terminal. Nesse e-mail, há um link que leva a uma página onde o usuário pode inserir sua nova senha. Como a recuperação é feita pelo terminal, não está disponível pelo site, mas pode ser testada localmente. Para isso, clique em "Esqueci senha".

<div align="center">
<img src="https://github.com/user-attachments/assets/c04c351f-9a68-4cc6-95da-aaede1142b24" width="700px" />
</div>

Digite o e-mail relacionado à sua conta.

<div align="center">
<img src="https://github.com/user-attachments/assets/c1e84579-8eaa-430a-9125-0fb64191db9d" width="700px" />
</div>

Ao seguir o link enviado no terminal, você será redirecionado para a página abaixo, onde poderá redefinir a sua senha. 

<div align="center">
<img src="https://github.com/user-attachments/assets/bfb3771f-6328-42ca-b55a-6ea5b970ccc7" width="700px" />
</div>

Após digitar sua nova senha, clique em "Redefinir senha" e pronto.

### 7. Exclusão de cápsulas do tempo
Para excluir uma cápsula, basta clicar em "Excluir" e confirmar a sua escolha. 

<div align="center">
<img width="1128" height="575" alt="image" src="https://github.com/user-attachments/assets/94b7a24e-5133-4fc3-9fcf-5b84ebecafb5" width="700px"/>
</div>

### 8. Exclusão de conta
Para excluir sua conta, vá para a edição do perfil (ver seção 3), clique em "Excluir conta" e confirme sua escolha. 

<div align="center">
<img alt="image" src="https://github.com/user-attachments/assets/c0fe6669-8587-4807-831c-a4d9104538d0" width="400px" />
</div>

</div>

## Sobre a abertura das cápsulas do tempo
Ao criar uma cápsula, ela permanecerá selada até a sua data de abertura. Portanto, não será possível visualizar o conteúdo de uma cápsula imediatamente após a sua criação. No entanto, é possível editar o conteúdo por meio de uma senha, definida no momento da criação. Para mais informações sobre isso, veja as seções 4 (Criação de cápsulas do tempo) e 5 (Edição de cápsulas do tempo). Assim que passar a data de abertura de uma cápsula, seu conteúdo poderá ser aberto e ficará disponível para ser visualizado sempre que desejar, mas não poderá mais ser editado. 


---

