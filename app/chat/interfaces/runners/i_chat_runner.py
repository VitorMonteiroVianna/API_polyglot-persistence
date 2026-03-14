from abc import ABC

from app.chat.model import SendMessagePayload


class IChatRunner(ABC):
    def run(self, payload: SendMessagePayload):
        raise NotImplementedError()
