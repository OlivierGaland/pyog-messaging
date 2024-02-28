class Client():
    DEFAULT_CLIENT_NAME = 'Clt'

    def __init__(self,server_addr,**kwargs):
        self.name = Client.DEFAULT_CLIENT_NAME if 'name' not in kwargs.keys() else kwargs['name']
        self.server_addr = server_addr
        self.callback = self._process_msg if 'callback' not in kwargs.keys() else kwargs['callback']

    def _process_msg(self,msg):
        return msg.execute()  

    def _get_socket(self):
        raise Exception("Not implemented")

    def _send(self,sock,msg):
        raise Exception("Not implemented")

    def _receive(self,sock):
        raise Exception("Not implemented")
