import socketserver
from og_messaging.net.svr.server import Server
from og_messaging.net.svr.udp.handler import ThreadedUDPRequestHandler

class ThreadedUDPServer(Server, socketserver.ThreadingMixIn, socketserver.UDPServer):

    def __init__(self,addr,**kwargs):
        self.callback = self._process_msg if 'callback' not in kwargs.keys() else kwargs['callback']
        super().__init__(addr,ThreadedUDPRequestHandler,**kwargs)

