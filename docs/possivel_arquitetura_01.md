# 🏗️ Arquitetura Simples Baseada em DDD (Domain-Driven Design)

Esta arquitetura organiza o projeto **por domínio**, mantendo as responsabilidades isoladas e promovendo modularidade, sem a complexidade total da arquitetura hexagonal.

---

## 📂 Estrutura de Pastas (DDD Simplificado)

```bash
project/
│── app/
│   ├── chat/
│   │   ├── entities/            # Entidades do domínio de chat
│   │   │   ├── chat.py
│   │   │   └── message.py
│   │   ├── repositories/        # Implementações de repositórios
│   │   │   ├── mongo_chat_repo.py
│   │   │   └── chroma_vector_repo.py
│   │   ├── services/            # Lógica de negócio do chat
│   │   │   └── chat_service.py
│   │   └── routers/             # Endpoints relacionados ao chat
│   │       └── chat_router.py
│   │
│   ├── users/
│   │   ├── entities/
│   │   │   └── user.py
│   │   ├── repositories/
│   │   │   └── postgres_user_repo.py
│   │   ├── services/
│   │   │   └── user_service.py
│   │   └── routers/
│   │       └── users_router.py
│   │
│   ├── auth/
│   │   ├── services/
│   │   │   └── auth_service.py   # JWT, login, signup
│   │   └── routers/
│   │       └── auth_router.py
│   │
│   ├── llm/
│   │   ├── services/
│   │   │   └── openrouter_llm_service.py
│   │   └── ports/               # Opcional: interface LLM
│   │
│   ├── infrastructure/
│   │   ├── db/
│   │   │   ├── postgres.py
│   │   │   ├── mongodb.py
│   │   │   ├── redis.py
│   │   │   └── chromadb.py
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── main.py                  # Ponto de entrada FastAPI
│   └── __init__.py
│
├── tests/
├── requirements.txt
├── .env
└── README.md
```

# ✅ Pontos Positivos da Arquitetura DDD Simplificada

1. **Organização por domínio**
   - Cada módulo concentra todas as entidades, serviços, repositórios e endpoints relacionados.
   - Facilita manutenção e compreensão do sistema.

2. **Modularidade**
   - Novas funcionalidades podem ser adicionadas criando novos domínios ou expandindo os existentes sem impactar outros domínios.

3. **Clareza de responsabilidades**
   - Entidades, serviços e repositórios estão agrupados por contexto, evitando mistura de lógica de negócio com detalhes técnicos.

4. **Facilidade de desenvolvimento inicial**
   - Estrutura menos complexa que Hexagonal, ideal para MVPs e projetos que precisam de resultados rápidos.

5. **Escalável de forma moderada**
   - É possível crescer o projeto adicionando novos domínios ou subdomínios de forma organizada.

6. **Integração direta com FastAPI**
   - Cada domínio pode expor seus próprios routers, simplificando o desenvolvimento de endpoints REST.

7. **Separação de persistência**
   - Mesmo com DDD simplificado, cada domínio pode ter seus repositórios (SQL, NoSQL, cache, vetorial) sem misturar com outros domínios.

8. **Flexibilidade para LLMs**
   - Serviços de LLM podem ser implementados dentro do domínio `llm/` ou injetados nos domínios que precisarem (chat, análise, etc.).


## 🔹 Plano de Implementação — Arquitetura DDD Simplificada

### **Fase 1 — Estrutura Base Funcional**

1. **Configuração do projeto**
   - Criar virtualenv/poetry/pipenv.
   - Instalar dependências: `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `pydantic`, `httpx`, `python-jose`, `motor`, `python-dotenv`.

2. **Estrutura de pastas**
   - Criar pastas por domínio: `chat/`, `users/`, `auth/`, `llm/`.
   - Criar subpastas: `entities/`, `repositories/`, `services/`, `routers/`.
   - Criar `infrastructure/` para bancos, config e segurança.
   - Criar `main.py` como ponto de entrada FastAPI.

3. **Endpoints vazios**
   - Criar routers FastAPI para cada domínio:
     - `auth_router.py`: `/signup`, `/login`.
     - `users_router.py`: `/users/me`.
     - `chat_router.py`: `/chat/send`, `/chat/history`.
   - Adicionar placeholders vazios para todos os endpoints.

4. **Implementação de usuários com JWT**
   - Criar entidades (`users/entities/user.py`).
   - Criar repositório Postgres (`users/repositories/postgres_user_repo.py`).
   - Implementar `auth_service.py`:
     - Signup (hash de senha)
     - Login (validação de senha)
     - Geração de JWT
   - Integrar Postgres com FastAPI (`infrastructure/db/postgres.py`).

5. **Serviço de envio para LLM (OpenRouter)**
   - Criar serviço em `llm/services/openrouter_llm_service.py`.
   - Implementar função `send_prompt(model, messages, api_key)`.
   - Integrar ao domínio de chat para envio de mensagens.

6. **Salvar comunicação no MongoDB**
   - Criar repositório Mongo (`chat/repositories/mongo_chat_repo.py`).
   - Salvar cada request/resposta enviada ao LLM.
   - Integrar `chat_service.py` para orquestrar envio e armazenamento.

---

### **Fase 2 — Performance e Customizações**

1. **Cache para GET de chats**
   - Criar repositório Redis (`chat/repositories/redis_cache_repo.py`).
   - Adicionar lógica de cache em `chat_service.py`:
     - Primeiro verifica cache para `GET /chat/history`.
     - Se não existe, busca no MongoDB e salva no cache.

2. **Processo de embeddings**
   - Criar repositório vetorial (`chat/repositories/chroma_vector_repo.py` ou FAISS).
   - Implementar serviço de embeddings vinculado ao `user_id`.
   - Atualizar `chat_service.py` para salvar embeddings a cada prompt.

3. **RAG — Recuperação de informações**
   - Buscar embeddings relacionados antes de enviar prompt ao LLM.
   - Incorporar informações recuperadas ao prompt.
   - Atualizar fluxo em `chat_service.py`.

4. **Testes básicos**
   - Testar signup/login (Postgres + JWT).
   - Testar envio de mensagem + armazenamento MongoDB.
   - Testar cache Redis.
   - Testar geração e recuperação de embeddings.
