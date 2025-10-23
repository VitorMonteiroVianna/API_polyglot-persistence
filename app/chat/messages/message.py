from dataclasses import dataclass, field, asdict
from abc import ABC

from app.shared import utils

from app.genai.available_models import AvailableModels


@dataclass(kw_only=True)
class Message(ABC):
    """
    Classe usada como base ser herdada por qualque classe que for
    armazenar uma mensagem do chat.
    """
    text: str
    genai_model: AvailableModels
    message_id: str = field(default_factory=lambda: utils.generate_hash_id())

    def as_dict(self) -> dict:
        data = asdict(self)
        if hasattr(self.genai_model, "value"):
            data["genai_model"] = self.genai_model.value
        return data
