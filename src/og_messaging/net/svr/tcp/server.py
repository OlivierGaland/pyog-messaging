import socketserver
from og_messaging.net.svr.server import Server
from og_messaging.net.svr.tcp.handler import ThreadedTCPRequestHandler,ThreadedTCPPersistentRequestHandler

class ThreadedTCPServer(Server, socketserver.ThreadingMixIn, socketserver.TCPServer):

    def __init__(self,addr,**kwargs):
        super().__init__(addr,ThreadedTCPRequestHandler,**kwargs)


class ThreadedPersistentTCPServer(Server, socketserver.ThreadingMixIn, socketserver.TCPServer):
    CNX_DURATION = 30
    CNX_TIMEOUT = 10

    def __init__(self,addr,**kwargs):
        self.callback = self._process_msg if 'callback' not in kwargs.keys() else kwargs['callback']
        self.cnx_duration = ThreadedPersistentTCPServer.CNX_DURATION if 'cnx_duration' not in kwargs.keys() else kwargs['cnx_duration']
        self.cnx_timeout = ThreadedPersistentTCPServer.CNX_TIMEOUT if 'cnx_timeout' not in kwargs.keys() else kwargs['cnx_timeout']
        super().__init__(addr,ThreadedTCPPersistentRequestHandler,**kwargs)

