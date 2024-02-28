class Message(Exception):

    @property
    def is_error(self):
        return False

    def __init__(self,**kwargs):
        self.payload = None if 'payload' not in kwargs.keys() else kwargs['payload']
    
    def execute(self,**kwargs):
        raise Exception("Not implemented")
    
    def __str__(self):
        return str(self.__class__.__name__) + ((", payload : " + str(self.payload)) if self.payload is not None else "")
        
class QueryMessage(Message): pass

class ReplyMessage(Message):

    def execute(self,**kwargs):
        pass

class ErrorMessage(Message):

    def __init__(self,code,description,**kwargs):
        self.code = code
        self.description = description
        super().__init__(**kwargs)

    @property
    def is_error(self):
        return True

    def execute(self,**kwargs):
        raise Exception("Reply Error : " + str(self.code) + " - " + str(self.description))
