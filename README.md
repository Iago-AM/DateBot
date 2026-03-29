# 🎓 Discord Academic Bot

Um bot para Discord criado para facilitar o gerenciamento de alunos em servidores acadêmicos — automatizando cadastro, verificação e controle de cargos.

---

## ✨ O que esse bot faz?

* 📩 Cadastro de alunos via `/login`
* 🔎 Verificação automática com base em uma planilha
* 🎭 Atribuição automática de cargos
* 🔒 Respostas privadas (ephemeral)
* 🛠️ Comandos administrativos para gerenciamento manual

---

## 🚀 Como usar

### 1. Clone ou baixe o projeto

```bash
https://github.com/Iago-AM/DateBot.git
```

Ou simplesmente baixe o `.zip` pelo GitHub.

---

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 3. Configure o bot

Antes de rodar, você precisa configurar algumas coisas importantes

---

## ⚙️ Configuração obrigatória

### 🔐 Token do bot

Crie um bot no Discord Developer Portal e copie o token.

Depois, crie um arquivo `.env` na raiz do projeto:

```env
DISCORD_TOKEN=seu_token_aqui
```

---

### 📊 Arquivo de dados (planilha)

O bot usa uma planilha `.xlsx` para validar os alunos.

Você deve criar um arquivo (ex: `alunos.xlsx`) com o seguinte formato:

| NOME COMPLETO | CURSO      | MATRICULA | DISCORD |
| ------------- | ---------- | --------- | ------- |
| João da Silva | Engenharia | 123456    | 0       |

📌 Regras:

* O nome deve estar **em maiúsculo** ou será convertido
* A coluna `DISCORD` deve começar com `0`
* O bot vai preencher automaticamente com o ID do usuário

---

### 📁 Definir o caminho do arquivo

No `.env`:

```env
DATA_FILE=alunos.xlsx
```

---

### 📢 Canal de logs

O bot envia logs de cadastro em um canal específico.

No `.env`:

```env
LOG_CHANNEL_ID=123456789012345678
```

👉 Para pegar o ID:

1. Ative o modo desenvolvedor no Discord
2. Clique com botão direito no canal
3. Copie o ID

---

### 🎭 Cargos necessários

Você precisa criar manualmente estes cargos no servidor e substituí-los no código:

* `NOME_REGISTRADO` → para usuários verificados
* `NOME_NAO_REGISTRADO` → para usuários não cadastrados
* `NOME_DO_CARGO` ou `Date` → para administradores do bot

---

## ▶️ Executando o bot

```bash
python main.py
```

Se tudo estiver certo, você verá:

```bash
Logado como SeuBot#1234
```

---

## 💬 Comandos disponíveis

### 👤 Usuário

* `/login`
  Inicia o processo de cadastro via DM

---

### 🛠️ Administração

* `/registrar`
  Registra um aluno manualmente

* `/limpar`
  Apaga mensagens do canal

---

## ⚠️ Observações importantes

* Este repositório **não inclui dados reais**
* O uso com dados pessoais deve respeitar a Lei Geral de Proteção de Dados Pessoais
* O bot depende de permissões corretas no servidor (roles e canais)

---

## 🧠 Possíveis melhorias

* Banco de dados (SQLite ou PostgreSQL)
* Sistema de logs mais robusto

---

## 🤝 Contribuições

Sinta-se à vontade para abrir issues ou pull requests!

---
