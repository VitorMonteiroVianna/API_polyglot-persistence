from app.users.models import User

from app.chat.models.message import SendMessage

from app.genai.handler import GenaiHander


class ChatRunner:

    def __init__(self, user: User):
        self.user = user
        self.genai_handler: GenaiHander= self.start_genai_hander()

    def start_genai_hander(self):
        return GenaiHander(user= self.user)
    
    def run(self, payload: SendMessage):

        genai_res = self.genai_handler.get_completions(
            message= payload.prompt,
            model=payload.genai_model
        )
        
        return {"res": genai_res.model_dump()}
        
    def send():
        # TODO: aqui vai vir o processo de enviar uma mensagem
        ...