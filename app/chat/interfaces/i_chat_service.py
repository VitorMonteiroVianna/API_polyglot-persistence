from abc import ABC


class IChatService(ABC):
    async def send_message(self, user_id: str, payload) -> dict:
        raise NotImplementedError()

    async def get_history(self, user_id: str, conversation_id: str) -> list[dict]:
        raise NotImplementedError()
