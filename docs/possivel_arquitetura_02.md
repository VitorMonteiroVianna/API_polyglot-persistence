# 🏗️ Arquitetura 01

O projeto segue a **Arquitetura Hexagonal (Ports & Adapters)**, garantindo **desacoplamento**, **testabilidade** e **flexibilidade** para trocar bancos de dados ou serviços externos sem alterar a lógica de negócio.

### Camadas

- **Core (Domínio)** → Entidades, value objects, casos de uso (regras de negócio puras).  
- **Ports (Interfaces)** → Contratos que definem como o domínio interage com bancos ou serviços externos.  
- **Adapters (Implementações)** → Implementam os ports para bancos de dados e LLMs.  
- **Application (Orquestração)** → Serviços que coordenam os casos de uso e adapters.  
- **Infrastructure** → Conexões com bancos, configuração e segurança (JWT, hashing).  
- **Entrypoints** → API REST com FastAPI.

---

## 📂 Estrutura de Pastas

```bash
project/
│── app/
│   ├── core/
│   │   ├── entities/
│   │   │   ├── user.py
│   │   │   ├── chat.py
│   │   │   └── message.py
│   │   ├── value_objects/
│   │   │   └── apikey.py
│   │   └── use_cases/
│   │       ├── send_message.py
│   │       ├── get_chat_history.py
│   │       └── register_user.py
│   │
│   ├── ports/
│   │   ├── user_repository.py
│   │   ├── chat_repository.py
│   │   ├── vector_repository.py
│   │   ├── cache_repository.py
│   │   └── llm_service.py
│   │
│   ├── adapters/
│   │   ├── repositories/
│   │   │   ├── postgres_user_repo.py
│   │   │   ├── mongo_chat_repo.py
│   │   │   ├── redis_cache_repo.py
│   │   │   └── chroma_vector_repo.py
│   │   └── services/
│   │       └── openrouter_llm_service.py
│   │
│   ├── application/
│   │   ├── auth_service.py
│   │   ├── chat_service.py
│   │   └── user_service.py
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
│   ├── entrypoints/
│   │   ├── api/
│   │   │   ├── auth_router.py
│   │   │   ├── chat_router.py
│   │   │   └── users_router.py
│   │   └── main.py
│   │
│   └── __init__.py
│
├── tests/
├── requirements.txt
├── .env
└── README.md
```

## Porque usar arquitetura hexagonal?

# ✅ Pontos Positivos da Arquitetura Hexagonal (Ports & Adapters)

1. **Desacoplamento total do domínio**
   - A lógica de negócio (core) não depende de frameworks, bancos de dados ou serviços externos.
   - Facilita manutenção e evolução do sistema sem afetar o domínio.

2. **Facilidade para trocar implementações externas**
   - Para mudar Postgres → MongoDB ou OpenRouter → LangChain, basta criar um novo adapter.
   - O domínio continua intacto, sem precisar alterar casos de uso ou entidades.

3. **Testabilidade aprimorada**
   - Possibilidade de mockar ports durante testes.
   - Testes de unidade focam apenas na lógica de negócio, sem depender de bancos ou APIs externas.

4. **Escalabilidade e modularidade**
   - Cada port e adapter é isolado, permitindo crescimento do projeto sem acoplamento.
   - Novas funcionalidades (ex: novos bancos, novos LLMs) podem ser adicionadas sem quebrar o sistema.

5. **Clareza e organização**
   - Separação de responsabilidades bem definida (core, ports, adapters, entrypoints, infrastructure).
   - Facilita onboarding de novos desenvolvedores e documentação do sistema.

6. **Segurança e controle**
   - Informações sensíveis, como APIKeys ou dados do usuário, podem ser centralizadas nos adapters e tratados de forma segura, sem poluir a lógica de negócio.

7. **Flexibilidade para múltiplas interfaces**
   - Um mesmo domínio pode ser exposto via REST, gRPC, CLI ou qualquer outro meio sem modificar a lógica interna.

8. **Facilidade de integração com múltiplos bancos**
   - Cada banco de dados (SQL, NoSQL, cache, vetorial) é apenas um adapter.
   - O domínio não precisa saber qual tecnologia está sendo usada, apenas interage com o port correspondente.


## 🔹 Plano de Implementação

### **Fase 1 — Estrutura Base Funcional**

1. **Configuração do projeto**
   - Criar virtualenv/poetry/pipenv.
   - Instalar dependências: `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `pydantic`, `httpx`, `python-jose`, `motor`, `python-dotenv`.

2. **Estrutura de pastas**
   - Criar estrutura hexagonal conforme planejado.

3. **Endpoints vazios**
   - Criar routers FastAPI: `auth_router`, `chat_router`, `users_router`.
   - Adicionar placeholders para endpoints (`/signup`, `/login`, `/chat/send`, `/chat/history`, `/users/me`).

4. **Implementação de usuários com JWT**
   - Criar entidades (`core/entities/user.py`).
   - Criar port `UserRepositoryPort`.
   - Criar adapter `PostgresUserRepo`.
   - Implementar `auth_service.py`:
     - Signup (hash de senha)
     - Login (validação de senha)
     - Geração de JWT
   - Integrar Postgres com FastAPI (`infrastructure/db/postgres.py`).

5. **Serviço de envio para LLM (OpenRouter)**
   - Criar port `LLMServicePort`.
   - Criar adapter `OpenRouterLLMService`.
   - Implementar função `send_prompt(model, messages, api_key)`.

6. **Salvar comunicação no MongoDB**
   - Criar port `ChatRepositoryPort`.
   - Criar adapter `MongoChatRepo`.
   - Salvar cada request/resposta enviada ao LLM no MongoDB.
   - Integrar `chat_service.py` para orquestrar envio e armazenamento.

---

### **Fase 2 — Performance e Customizações**

1. **Cache para GET de chats**
   - Criar port `CacheRepositoryPort`.
   - Criar adapter `RedisCacheRepo`.
   - Adicionar lógica de cache em `chat_service.py`.

2. **Processo de embeddings**
   - Criar port `VectorRepositoryPort`.
   - Criar adapter `ChromaVectorRepo` (ou FAISS).
   - Implementar serviço de embeddings vinculado ao `user_id`.

3. **RAG — Recuperação de informações**
   - Buscar embeddings relacionados antes de enviar prompt ao LLM.
   - Incorporar informações recuperadas ao prompt.
   - Atualizar `chat_service.py` para incluir essa etapa.

4. **Testes básicos**
   - Signup/login (Postgres + JWT).
   - Envio de mensagem + armazenamento MongoDB.
   - Cache Redis.
   - Geração e recuperação de embeddings.
