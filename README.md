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

---

## Relatório de Testes

---
