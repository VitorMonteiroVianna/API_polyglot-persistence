from abc import ABC


class IMessage(ABC):
    def as_dict(self) -> dict:
        raise NotImplementedError()
