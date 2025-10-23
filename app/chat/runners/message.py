from app.users.models import User

from app.chat.model import SendMessagePayload

from app.genai.handler import GenaiHander

from app.chat.messages import UserMessage, GenaiMessage



class ChatRunner:

    def __init__(self, user: User):
        self.user = user
        self.genai_handler: GenaiHander= self.start_genai_hander()

    def run(self, payload: SendMessagePayload):

        user_message = self.create_user_message(payload)
        genai_res = self.get_genai_response(user_message)
        
        return {"res": genai_res.as_dict()}
    
    
    def start_genai_hander(self):
        return GenaiHander(user= self.user)

    def create_user_message(self, payload: SendMessagePayload) -> UserMessage:
        return UserMessage(
            text= payload.prompt,
            genai_model= payload.genai_model,
            max_tokens= self.MAX_TOKENS,
            temperature= self.TEMPERATURE
        )

    def get_genai_response(self, user_message: UserMessage) -> GenaiMessage:
        return self.genai_handler.get_completions(user_message=user_message)
    
