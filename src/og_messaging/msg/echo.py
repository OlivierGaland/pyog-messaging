from og_log import LOG
from og_messaging.msg.message import QueryMessage,ReplyMessage,ErrorMessage

class EchoQuery(QueryMessage):
    def execute(self,**kwargs):
        return EchoReply(payload={'msg':self.payload['msg']})

class EchoReply(ReplyMessage):
    pass

