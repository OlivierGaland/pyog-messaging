import socketserver
from og_messaging.net.svr.server import Server
from og_messaging.net.svr.udp.handler import ThreadedUDPRequestHandler

class ThreadedUDPServer(Server, socketserver.ThreadingMixIn, socketserver.UDPServer):

    def __init__(self,addr,**kwargs):
        super().__init__(addr,ThreadedUDPRequestHandler,**kwargs)

