# API_polyglot-persistence



## Ideia do projeto:

- Uma API de chat de IA. 
    - A API deve ter login usando JWT (usuario salvo no SQL)
    - A API vai salvar o historico de chat (chat salvo no noSQL)
    - A API pode busacar pelas mensagens que um chat ja teve (noSQL + cache a partir da segunda chamada)
    - A API pode salvar preferencias do usaurio no banco vetorial usando o processo de Embedding


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
        "user_id": "",
        "chat_id": "",
        "prompt": "",
        "model": ""
      }
      ```

- **GET /chat**
    - Retorna o histórico do chat e tokens consumidos.
    - Parâmetros:
      - `chat_id` (query)
      - Requer JWT no header.


## FLUXO PREVISTO - ENVIO DE PROMPT

- Faz o enriquecimento do prompt usando o banco vetorial e o user_id:
	- Busca no banco vetorial se tem algum dado que agregue nesse prompt

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

