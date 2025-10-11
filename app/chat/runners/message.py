from app.users.models import User

from app.genai.handler import GenaiHander


class MessageRunner:

    def __init__(self, user: User):
        self.user = user
        self.genai_handler: GenaiHander= self.start_genai_hander()

    def start_genai_hander(self):
        return GenaiHander(user= self.user)
    
    def run(self):
        message = "me conta uma piada legal"
        genai_res = self.genai_handler.get_completions(message)
        
        return {"res": genai_res}
        
    def send():
        # TODO: aqui vai vir o processo de enviar uma mensagem
        ...