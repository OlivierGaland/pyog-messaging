from og_messaging.msg.message import QueryMessage,ReplyMessage

class PingQuery(QueryMessage):
    def execute(self,**kwargs):
        return PingReply()

class PingReply(ReplyMessage): pass
