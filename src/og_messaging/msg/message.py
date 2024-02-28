class Message(Exception):

    def __init__(self,**kwargs):
        self.payload = None if 'payload' not in kwargs.keys() else kwargs['payload']
    
    def execute(self,**kwargs):
        raise Exception("Not implemented")

    def send(self,addr):
        raise Exception("Not implemented")
    
    def __str__(self):
        return str(self.__class__.__name__) + ((", payload : " + str(self.payload)) if self.payload is not None else "")
        
class QueryMessage(Message): pass

class ReplyMessage(Message):

    def execute(self,**kwargs):
        pass

