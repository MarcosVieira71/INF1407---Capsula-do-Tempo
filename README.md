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
- Deploy do site.

---

## Instruções de uso

### 1. Acesso via site 
Para testar a aplicação diretamente no navegador, acesse o link:
👉 **(https://capsuladotempo.onrender.com/)**

### 2. Execução em ambiente local
Caso deseje rodar o projeto em sua máquina, certifique-se de que tem o Python instalado e siga os passos:

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

<img width="1351" height="716" alt="image" src="https://github.com/user-attachments/assets/0ba0552a-1e8a-407a-8de8-fba8e6939627" />

Preencha todos os campos do formulário e clique em "Cadastrar".

<img width="1237" height="875" alt="image" src="https://github.com/user-attachments/assets/0925034e-2cde-4294-b62a-671b822abb39" />

Se os campos tiverem sido preenchidos corretamente, você será direcionado à página de login. Caso contrário, corrija os campos que estiverem indicados com erro no formulário. 

### 2. Login

A opção de login pode ser acessada através da página inicial clicando em "Login".

<img width="1529" height="760" alt="image" src="https://github.com/user-attachments/assets/dc6aa41a-1196-4869-a2e5-844257bdee95" />

Preencha o formulário com o username e a senha que você criou ao se registrar no site. Caso tenha esquecido a sua senha, veja a seção "Recuperação de senha".

<img width="1259" height="834" alt="image" src="https://github.com/user-attachments/assets/8efe8a51-1f1a-4c13-80c9-a3aa6e1c21bc" />

### 3. Edição do perfil
Para editar seu perfil, clique em "Olá, [seu username] ou na imagem da moldura no topo direito do site.

<img width="1714" height="382" alt="image" src="https://github.com/user-attachments/assets/8896411e-c461-42f5-ad88-709a3375bda1" />

Altere as informações que desejar por meio do formulário e clique em "Salvar" ou clique em "Alterar senha" caso deseje trocar a sua senha.

<img width="684" height="793" alt="image" src="https://github.com/user-attachments/assets/dc184633-8161-4cc5-a61a-bc73677d9bd1" />

Para alterar a sua senha, insira a senha antiga e confirme. 

<img width="637" height="897" alt="image" src="https://github.com/user-attachments/assets/40f88264-18f7-4465-a8f7-9507ffcab616" />

### 4. Criação de cápsulas do tempo
Para criar uma cápsula do tempo, você precisa estar logado. Para mais informações sobre registro e login, veja as seções 1 e 2. Quando estiver pronto, clique em "Criar cápsula".

<img width="984" height="618" alt="image" src="https://github.com/user-attachments/assets/5e7a025d-def9-4e6f-b4ee-657bf27a01ab" />

Preencha a sua cápsula com título, data de abertura e um texto para o seu futuro eu. Além disso, crie uma senha para a sua cápsula. Caso deseje editá-la, será necessário inserir essa senha. 

<img width="728" height="879" alt="image" src="https://github.com/user-attachments/assets/6f04a38d-648f-4fc2-a3f9-cd338d07f8d3" />

Assim que você criar uma cápsula, ela ficará salva no seu perfil. Para ver todas as suas cápsulas criadas, basta clicar em "Cápsulas". 

<img width="1259" height="727" alt="image" src="https://github.com/user-attachments/assets/b2276c0c-63d6-4d2f-bc9b-54a2080c54de" />

### 5. Edição de cápsulas do tempo
Para editar uma cápsula do tempo, clique em "Editar". É necessário inserir a senha que você definiu no momento da criação. 

<img width="438" height="372" alt="image" src="https://github.com/user-attachments/assets/04728ae3-e46a-40c3-a479-54f67e2d9832" />

<img width="472" height="659" alt="image" src="https://github.com/user-attachments/assets/7e51a6e6-79d5-4774-9973-2f8c0aabbb97" />

<img width="431" height="596" alt="image" src="https://github.com/user-attachments/assets/146d9efe-b103-49ad-92d4-9fa163f56761" />


Quando estiver satisfeito com as suas mudanças, clique em "Salvar".

### 6. Recuperação de senha

---

## Relatório de Testes

---

