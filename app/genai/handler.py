from typing import Dict

from app.services.interfaces.i_open_router_service import IOpenRouterService

from app.genai.available_models import AvailableModels

from app.chat.messages import UserMessage, GenaiMessage
from app.chat.tokens import CompletionTokenDetails, GenaiModelUsage
from app.genai.interfaces.i_genai_hander import IGenaiHander


class GenaiHander(IGenaiHander):
    def __init__(self, open_router_service: IOpenRouterService):
        self.__open_router = open_router_service

    def __create_genai_message_from_open_router_res(
        self, open_router_res: Dict, user_message: UserMessage
    ) -> GenaiMessage:
        """
        Cria um objeto GenaiMessage a partir da resposta retornada pelo
        OpenRouter.
        """
        choice = open_router_res["choices"][0]
        usage = open_router_res.get("usage", {})
        resolved_model = self.__resolve_model(
            model_from_response=open_router_res.get("model"),
            requested_model=user_message.genai_model,
        )

        return GenaiMessage(
            text=choice["message"]["content"],
            genai_model=resolved_model,
            conversation_id=user_message.conversation_id,
            user_message_id=user_message.message_id,
            genai_role=choice["message"]["role"],
            genai_usage=GenaiModelUsage(
                prompt_tokens=usage.get("prompt_tokens", 0),
                completion_tokens=usage.get("completion_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
                completion_tokens_details=CompletionTokenDetails(**usage.get("completion_tokens_details", {}))
                if usage.get("completion_tokens_details")
                else None,
            ),
        )

    def __resolve_model(self, model_from_response: str | None, requested_model: AvailableModels) -> AvailableModels:
        """
        Normaliza o modelo retornado pelo OpenRouter para um valor existente
        em `AvailableModels`.
        """
        if not model_from_response:
            return requested_model

        try:
            return AvailableModels(model_from_response)
        except ValueError:
            pass

        for model in AvailableModels:
            if model_from_response.startswith(model.value):
                return model

        return requested_model

    def get_completions(
            self,
            user_message: UserMessage
    ) -> GenaiMessage:

        open_router_res = self.__open_router.generate_response(
            message = user_message.text,
            model= user_message.genai_model,
            max_tokens= user_message.max_tokens,
            temperature= user_message.temperature,
        )
        genai_message = self.__create_genai_message_from_open_router_res(
            open_router_res = open_router_res,
            user_message = user_message
        )

        return genai_message

    def get_embedding(self, text: str, model: AvailableModels) -> list[float]:
        """
        Gera um vetor de embedding para o texto informado.
        Implementado via OpenRouter.
        """
        return self.__open_router.generate_embedding(text, model)
