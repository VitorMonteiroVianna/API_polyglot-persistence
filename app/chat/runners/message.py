from app.users.models import User

from app.chat.model import SendMessagePayload

from app.genai.interfaces.i_genai_hander import IGenaiHander

from app.chat.messages import UserMessage, GenaiMessage
from app.shared import utils

from app.chat.interfaces.runners.i_chat_runner import IChatRunner
from app.chat.interfaces.runners.i_embedding_runner import IEmbeddingRunner


class ChatRunner(IChatRunner):

    def __init__(
        self,
        user: User,
        genai_handler: IGenaiHander,
        embedding_runner: IEmbeddingRunner,
    ):
        self.__user = user
        self.__genai_handler = genai_handler
        self.__embedding_runner = embedding_runner

    def run(self, payload: SendMessagePayload):

        if payload.use_embedding:
            payload.prompt = self.__embedding_runner.enrich_prompt(
                prompt=payload.prompt,
            )

        user_message = self.__create_user_message(payload)
        genai_res = self.__get_genai_response(user_message)

        return {"res": genai_res.as_dict()}

    def __create_user_message(self, payload: SendMessagePayload) -> UserMessage:
        return UserMessage(
            text=payload.prompt,
            genai_model=payload.genai_model,
            max_tokens=payload.max_tokens,
            temperature=payload.temperature,
            conversation_id=payload.chat_id or utils.generate_hash_id(),
            user_id=str(self.__user.id),
        )

    def __get_genai_response(self, user_message: UserMessage) -> GenaiMessage:
        return self.__genai_handler.get_completions(user_message=user_message)

