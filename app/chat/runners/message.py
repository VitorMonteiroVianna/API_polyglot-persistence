from app.users.models import User

from app.chat.model import SendMessage

from app.genai.handler import GenaiHander

from app.chat.messages import UserMessage, GenaiMessage


# TODO:
#
# Mudar o payload de entrada:
#   - Receber MAX_TOKENS e TEMPERATURE
#
#   **Recerber CHAT_ID pelo payload**
#     - Caso chat_id == None, criar um novo
#     - se passar um id, puxa do mongo

class ChatRunner:

    def __init__(self, user: User):
        self.user = user
        self.genai_handler: GenaiHander= self.start_genai_hander()
        
        self.MAX_TOKENS = 255 
        self.TEMPERATURE = 0.7

    def start_genai_hander(self):
        return GenaiHander(user= self.user)

    def create_user_message(self, payload: SendMessage) -> UserMessage:
        return UserMessage(
            text= payload.prompt,
            genai_model= payload.genai_model,
            max_tokens= self.MAX_TOKENS,
            temperature= self.TEMPERATURE
        )

    def get_genai_response(self, user_message: UserMessage) -> GenaiMessage:
        return self.genai_handler.get_completions(user_message=user_message)
    
    def run(self, payload: SendMessage):

        user_message = self.create_user_message(payload)
        genai_res = self.get_genai_response(user_message)
        
        return {"res": genai_res.as_dict()}
        