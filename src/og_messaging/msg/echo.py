from og_messaging.msg.message import QueryMessage,ReplyMessage

class EchoQuery(QueryMessage):
    def execute(self,**kwargs):
        return EchoReply(payload={'msg':self.payload['msg']})

class EchoReply(ReplyMessage):
    pass

