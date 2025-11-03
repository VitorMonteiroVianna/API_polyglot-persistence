# API_polyglot-persistence


Este projeto é uma **API em Python (FastAPI)** que permite a integração com **múltiplos modelos de LLM** (via [OpenRouter](https://openrouter.ai/)), fornecendo um **chat com histórico** e suporte a **múltiplos bancos de dados** e **embedding** que fica atrelado ao usuario.

## 🚀 Objetivo

Criar uma API que:
- Permita ao usuário conversar com diferentes LLMs de forma unificada.
- Armazene o histórico de conversas.
- Utilize diferentes tipos de banco de dados como requisito acadêmico/técnico.

## 🏗️ Arquitetura da Solução

- **FastAPI** → Framework principal para expor os endpoints.
- **JWT Authentication** → Controle de login e autenticação.
- **OpenRouter API** → Gateway único para acesso a múltiplos modelos (OpenAI, Claude, Gemini, etc).
- **Bancos de Dados**:
  - **Postgres** → Banco SQL para dados relacionais.
  - **MongoDB** → Banco NoSQL para dados flexíveis.
  - **Redis** → Cache e sessões rápidas.
  - **ChromaDB / FAISS** → Banco vetorial para embeddings e RAG. Ainda não escolhidos, mas ambos são soluções que rodam localmente e não precisam de um servidor/software externo atrelado.

## 🔑 Gestão da API Key do OpenRouter

Cada usuário precisa informar **sua própria APIKey do OpenRouter**.  
Essa chave é tratada de forma **segura, como uma senha**:

1. O usuário se cadastra e faz login (JWT).
2. Durante o cadastro, o usuário envia sua APIKey do OpenRouter.
3. A chave é armazenada no banco em um campo seguro (hash/criptografia).
4. Em cada request autenticada, o backend recupera a chave associada ao usuário e faz a chamada ao OpenRouter.
5. A chave **nunca é exposta diretamente** ao front-end após o cadastro.

## 📡 Fluxo de Requisição

1. Usuário faz login → recebe um **JWT**.
2. Usuário envia mensagens para `/chat`, escolhendo o modelo (ex.: `openai/gpt-4`).
3. O backend busca a APIKey segura do usuário no banco.
4. O backend repassa a requisição ao OpenRouter usando a chave do usuário.
5. A resposta do modelo é retornada para o cliente.

### Autenticação e Usuário

- **POST /register**
    - Cria um novo usuário.
    - Corpo:
      ```json
      {
        "username": "",
        "password": ""
      }
      ```

- **POST /login**
    - Autentica o usuário e retorna um JWT.
    - Corpo:
      ```json
      {
        "username": "",
        "password": ""
      }
      ```

- **GET /user/profile**
    - Retorna informações do usuário autenticado.
    - Requer JWT no header.

- **PUT /user/profile**
    - Atualiza informações do usuário autenticado.
    - Requer JWT no header.

---

### Chat

- **POST /chat**
    - Envia um prompt para o chat.
    - Corpo:
      ```json
      {
        "chat_id": "",
        "prompt": "",
        "model": ""
      }
      ```
    - **Observação:** O `user_id` não precisa ser enviado no corpo da requisição. Quando o JWT é enviado no header, o backend extrai o `user_id` diretamente do token, garantindo segurança e autenticidade do usuário.

- **GET /chat**
    - Retorna o histórico do chat e tokens consumidos.
    - Parâmetros:
      - `chat_id` (query)
      - Requer JWT no header.


## FLUXO PREVISTO - ENVIO DE PROMPT

- Faz o enriquecimento do prompt usando o banco vetorial e o user_id:
    - Busca no banco vetorial se tem algum dado que agregue nesse prompt
    - O user_id é obtido diretamente do JWT enviado no header, não sendo necessário passar pelo corpo da requisição.

- Faz o processo de embedidng:
    - Verifica se o prompt passado (antes do enriquecimento) contem algum informação que deve ser salva. ex: "sou um desenvolvedor de software" ou "fale comigo de maneira formal", basicamente preferencias de uso do usuario
    - O embedding vai para o banco vetorial

- Foi passado um chat_id?
    - Não (chat_id: ""):
        -Cria um chat:
            - Chat deve ser uma classe que contem alguns atributos internos, como tokens usados, mensagens (input e output) e horario de atualização
        - Sobe o chat no banco NOSQL
    - Sim:
        - Puxa no NOSQL o historico de mensagens para passar como contexto 

- Salva a resposta no NOSQL



## 🧭 Controle de Migrations

O projeto utiliza o **Alembic** para versionar e aplicar mudanças no banco de dados PostgreSQL hospedado no **Supabase** (com conexão via Pooler).

---

## ⚙️ Estrutura de Conexão

A conexão com o banco é feita através de variáveis definidas no arquivo `.env`:

```bash
DATABASE_URL=postgresql+psycopg2://postgres.<project-id>:<PASSWORD>@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require
```

> ⚠️ Importante: use sempre o **usuário com prefixo `postgres.<project-id>`** (como fornecido pelo Supabase).

---

## 🧩 Quando criar uma migration

Você deve gerar uma **nova migration** sempre que **alterar o modelo de dados** da aplicação — por exemplo:

- Criar ou remover uma tabela (`Base` de novos modelos SQLAlchemy)
- Adicionar, renomear ou excluir colunas
- Alterar relacionamentos (`ForeignKey`, `relationship`, etc.)
- Mudar constraints (unique, not null, default...)

Em resumo: **qualquer mudança em `models.py` que afete o schema do banco** precisa de uma migration.

---

## 🚀 Como criar e aplicar migrations

### 1️⃣ Gerar uma nova migration

Depois de atualizar seus modelos (por exemplo, `app/users/models.py`):

```bash
alembic revision --autogenerate -m "Descrição da mudança"
```

📄 Isso cria um novo arquivo de migration dentro da pasta `alembic/versions/`, contendo as instruções SQL para atualizar o banco.

---

### 2️⃣ Revisar o conteúdo da migration

Abra o arquivo gerado em `alembic/versions/xxxx_nome_da_migration.py` e verifique:

- Se as tabelas e colunas alteradas estão corretas  
- Se não há instruções desnecessárias ou faltantes  

💡 Dica: se estiver em dúvida, **nunca rode direto em produção**. Teste primeiro localmente ou em um banco de staging.

---

### 3️⃣ Aplicar as migrations no banco

Para aplicar todas as migrations pendentes:

```bash
alembic upgrade head
```

Isso executa as alterações no banco remoto (Supabase).

---

### 4️⃣ Reverter uma migration (opcional)

Se precisar voltar ao estado anterior:

```bash
alembic downgrade -1
```

ou para voltar a uma versão específica:

```bash
alembic downgrade <revision_id>
```

---

## 🧰 Comandos úteis

| Ação | Comando |
|------|----------|
| Ver histórico de migrations | `alembic history` |
| Mostrar versão atual do banco | `alembic current` |
| Criar nova migration | `alembic revision --autogenerate -m "mensagem"` |
| Aplicar migrations | `alembic upgrade head` |
| Reverter última migration | `alembic downgrade -1` |

---

## 🧩 Dicas adicionais

- Mantenha sempre a **estrutura de models e Base centralizada** (ex: `app/users/models.py`)  
- Use o `Base.metadata` importado no `env.py` para garantir que o Alembic veja todos os modelos  
- Se estiver usando múltiplos módulos com models, importe todos no `env.py` antes de definir `target_metadata`